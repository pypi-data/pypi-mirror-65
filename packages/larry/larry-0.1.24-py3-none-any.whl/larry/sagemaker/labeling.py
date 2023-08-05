import json
import boto3
import os
from larry import utils
from larry import s3
from botocore.exceptions import ClientError
from larry.utils.image import scale_image_to_size


client = None
# A local instance of the boto3 session to use
__session = boto3.session.Session()


def set_session(aws_access_key_id=None,
                aws_secret_access_key=None,
                aws__session_token=None,
                region_name=None,
                profile_name=None,
                boto_session=None):
    """
    Sets the boto3 session for this module to use a specified configuration state.
    :param aws_access_key_id: AWS access key ID
    :param aws_secret_access_key: AWS secret access key
    :param aws__session_token: AWS temporary session token
    :param region_name: Default region when creating new connections
    :param profile_name: The name of a profile to use
    :param boto_session: An existing session to use
    :return: None
    """
    global __session, client
    __session = boto_session if boto_session is not None else boto3.session.Session(**utils.copy_non_null_keys(locals()))
    __client = __session.client('sagemaker')


def build_pre_response(event, log_details=True, input_attribute='taskObject'):
    if log_details:
        print(event)
    source = event['dataObject'].get('source', event['dataObject'].get('source-ref'))
    if source is None:
        print('No source or source-ref value found')
        return {}
    if log_details:
        print('Task object is: {}'.format(source))
    response = {'taskInput': {}}
    response['taskInput'][input_attribute] = source
    if log_details:
        print('Response is {}'.format(json.dumps(response)))
    return response


def build_pre_response_from_object(event, log_details=True, input_attribute='taskObject', s3_resource=None):
    if log_details:
        print(event)
    source_ref = event['dataObject'].get('source-ref')
    if source_ref:
        if s3_resource:
            value = s3.read_dict(uri=source_ref, s3_resource=s3_resource)
        else:
            value = s3.read_dict(uri=source_ref)
    else:
        source = event['dataObject'].get('source')
        if source is None:
            print('No source or source-ref value found')
            return {}
        else:
            if type(source) is str:
                value = json.loads(source)
            else:
                value = source
    if log_details:
        print('Task object is: {}'.format(json.dumps(value)))
    response = {'taskInput': {}}
    response['taskInput'][input_attribute] = value
    if log_details:
        print('Response is {}'.format(json.dumps(response)))
    return response


def build_consolidation_response(event, log_details=True):
    if log_details:
        print(json.dumps(event))
    payload = get_payload(event)
    if log_details:
        print('Payload: {}'.format(json.dumps(payload)))

    consolidated_response = []
    for dataset in payload:
        responses = extract_worker_responses(dataset['annotations'])
        consolidated_response.append({
            'datasetObjectId': dataset['datasetObjectId'],
            'consolidatedAnnotation': {
                'content': {
                    event['labelAttributeName']: {
                        'responses': responses
                    }
                }
            }
        })
    if log_details:
        print('Consolidated response: {}'.format(json.dumps(consolidated_response)))
    return consolidated_response


def extract_worker_responses(annotations):
    responses = []
    for annotation in annotations:
        response = json.loads(annotation['annotationData']['content'])
        if 'annotatedResult' in response:
            response = response['annotatedResult']

        responses.append({
            'workerId': annotation['workerId'],
            'annotation': response
        })
    return responses


def get_payload(event):
    if 'payload' in event:
        return s3.read_dict(uri=event['payload']['s3Uri'])
    else:
        return event.get('test_payload', [])


def _input_config(manifest_uri, free_of_pii=False, free_of_adult_content=True):
    config = {
        'DataSource': {
            'S3DataSource': {
                'ManifestS3Uri': manifest_uri
            }
        }
    }
    content_classifiers = []
    if free_of_adult_content:
        content_classifiers.append('FreeOfAdultContent')
    if free_of_pii:
        content_classifiers.append('FreeOfPersonallyIdentifiableInformation')
    if len(content_classifiers) > 0:
        config['DataAttributes'] = {'ContentClassifiers': content_classifiers}
    return config


def _output_config(output_uri, kms_key=None):
    config = {
        'S3OutputPath': output_uri
    }
    if kms_key:
        config['KmsKeyId'] = kms_key
    return config


def build_human_task_config(template_uri, pre_lambda_arn, consolidation_lambda_arn, title, description, workers=1,
                            public=False, reward_in_cents=None, workteam_arn=None, time_limit=300, lifetime=345600,
                            max_concurrent_tasks=None, keywords=None, region=None):
    region = __session.region_name if region is None else region
    config = {
        'UiConfig': {
            'UiTemplateS3Uri': template_uri
        },
        'PreHumanTaskLambdaArn': pre_lambda_arn,
        'TaskTitle': title,
        'TaskDescription': description,
        'NumberOfHumanWorkersPerDataObject': workers,
        'TaskTimeLimitInSeconds': time_limit,
        'TaskAvailabilityLifetimeInSeconds': lifetime,
        'AnnotationConsolidationConfig': {
            'AnnotationConsolidationLambdaArn': consolidation_lambda_arn
        }
    }
    if public:
        config['WorkteamArn'] = 'arn:aws:sagemaker:{}:394669845002:workteam/public-crowd/default'.format(region)
        if reward_in_cents is None:
            raise Exception('You must provide a reward amount for a public labeling job')
        else:
            config['PublicWorkforceTaskPrice'] = {
                'AmountInUsd': {
                    'Dollars': int(reward_in_cents // 100),
                    'Cents': int(reward_in_cents),
                    'TenthFractionsOfACent': round((reward_in_cents % 1) * 10)
                }
            }
    elif workteam_arn is not None:
        config['WorkteamArn'] = workteam_arn
    else:
        raise Exception('Labeling job must be public or have a workteam ARN')
    if keywords:
        config['TaskKeywords'] = keywords
    if max_concurrent_tasks:
        config['MaxConcurrentTaskCount'] = max_concurrent_tasks
    return config


def build_stopping_conditions(max_human_labeled_object_count=None, max_percentage_labeled=None):
    if max_human_labeled_object_count is None or max_percentage_labeled is None:
        return None
    else:
        config = {}
        if max_human_labeled_object_count:
            config['MaxHumanLabeledObjectCount'] = max_human_labeled_object_count
        if max_percentage_labeled:
            config['MaxPercentageOfInputDatasetLabeled'] = max_percentage_labeled
        return config


def build_algorithms_config(algorithm_specification_arn, initial_active_learning_model_arn=None, kms_key=None):
    if algorithm_specification_arn is None:
        return None
    config = {
        'LabelingJobAlgorithmSpecificationArn': algorithm_specification_arn
    }
    if initial_active_learning_model_arn:
        config['InitialActiveLearningModelArn'] = initial_active_learning_model_arn
    if kms_key:
        config['LabelingJobResourceConfig'] = {'VolumeKmsKeyId': kms_key}
    return config


def create_job(name,
               manifest_uri,
               output_uri,
               role_arn,
               task_config,
               category_config_uri=None,
               label_attribute_name=None,
               free_of_pii=False,
               free_of_adult_content=True,
               algorithms_config=None,
               stopping_conditions=None,
               sagemaker_client=None):
    sagemaker_client = sagemaker_client if sagemaker_client else client
    if label_attribute_name is None:
        label_attribute_name = name
    params = {
        'LabelingJobName': name,
        'LabelAttributeName': label_attribute_name,
        'InputConfig': _input_config(manifest_uri, free_of_pii, free_of_adult_content),
        'OutputConfig': _output_config(output_uri),
        'RoleArn': role_arn,
        'HumanTaskConfig': task_config
    }
    if category_config_uri:
        params['LabelCategoryConfigS3Uri'] = category_config_uri
    if algorithms_config:
        params['LabelingJobAlgorithmsConfig'] = algorithms_config
    if stopping_conditions:
        params['StoppingConditions'] = stopping_conditions
    return sagemaker_client.create_labeling_job(**params)


def describe_job(name, sagemaker_client=None):
    sagemaker_client = sagemaker_client if sagemaker_client else client
    return sagemaker_client.describe_labeling_job(LabelingJobName=name)


def get_job_state(name, sagemaker_client=None):
    sagemaker_client = sagemaker_client if sagemaker_client else client
    response = describe_job(name, sagemaker_client)
    status = response['LabelingJobStatus']
    labeled = response['LabelCounters']['TotalLabeled']
    unlabeled = response['LabelCounters']['Unlabeled']
    failed = response['LabelCounters']['FailedNonRetryableError']
    fail_message = ' {} failed'.format(failed) if failed > 0 else ''
    return "{} ({}/{})".format(status, labeled, unlabeled + labeled)+fail_message


def get_worker_responses(output_uri, job_name):
    by_worker = {}
    by_item = {}
    bucket_name, k = s3.decompose_uri(output_uri)
    for response_key in s3.list_objects(uri=os.path.join(output_uri, job_name, 'annotations/worker-response')):
        response_obj = s3.read_dict(bucket_name, response_key)
        item_id = response_key.split('/')[-2]
        by_item[item_id] = response_obj
        for response in response_obj['answers']:
            worker_id = response['workerId']
            responses = by_worker.get(worker_id, [])
            response['itemId'] = item_id
            responses.append(response)
            by_worker[worker_id] = responses
    return by_item, by_worker


def get_results(output_uri, job_name):
    try:
        return s3.read_list_of_dict(uri=os.path.join(output_uri, job_name, 'manifests/output/output.manifest'))
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return []
        else:
            raise


def get_multiple_results(output_uri, job_names, rename_label_to=None, exclude_failures=True):
    cumulative_results = []
    for job_name in job_names:
        results = get_results(output_uri, job_name)
        for item in results:
            if item[job_name + '-metadata'].get('failure-reason') is None or exclude_failures is False:
                if rename_label_to:
                    item[rename_label_to] = item.pop(job_name)
                    item[rename_label_to + '-metadata'] = item.pop(job_name + '-metadata')
                cumulative_results.append(item)
    return cumulative_results


def find_failures(manifest, attribute_name):
    failures = []
    reasons = {}
    for item in manifest:
        failure_reason = item[attribute_name+'-metadata'].get('failure-reason')
        if failure_reason:
            failures.append(item)
            failure_reason = failure_reason.replace(item['source-ref'], '<file>')
            failure_reason = failure_reason.replace(item['source-ref'].replace('/', '\\/'), '<file>')
            cnt = reasons.get(failure_reason,0)
            reasons[failure_reason] = cnt + 1
    return failures, reasons


def built_in_pre_lambda_bounding_box(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('PRE', region, 'BoundingBox')


def built_in_pre_lambda_image_multi_class(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('PRE', region, 'ImageMultiClass')


def built_in_pre_lambda_semantic_segmentation(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('PRE', region, 'SemanticSegmentation')


def built_in_pre_lambda_text_multi_class(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('PRE', region, 'TextMultiClass')


def built_in_pre_lambda_named_entity_recognition(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('PRE', region, 'NamedEntityRecognition')


def built_in_acs_lambda_bounding_box(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('ACS', region, 'BoundingBox')


def built_in_acs_lambda_image_multi_class(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('ACS', region, 'ImageMultiClass')


def built_in_acs_lambda_semantic_segmentation(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('ACS', region, 'SemanticSegmentation')


def built_in_acs_lambda_text_multi_class(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('ACS', region, 'TextMultiClass')


def built_in_acs_lambda_named_entity_recognition(region=None):
    region = __session.region_name if region is None else region
    return _built_in_lambda('ACS', region, 'NamedEntityRecognition')


def _built_in_lambda(mode, region, task):
    accounts = {
        'us-east-1': '432418664414',
        'us-east-2': '266458841044',
        'us-west-2': '081040173940',
        'ca-central-1': '918755190332',
        'eu-west-1': '568282634449',
        'eu-west-2': '487402164563',
        'eu-central-1': '203001061592',
        'ap-northeast-1':'477331159723',
        'ap-northeast-2':'845288260483',
        'ap-south-1':'565803892007',
        'ap-southeast-1':'377565633583',
        'ap-southeast-2':'454466003867'
    }
    account_id = accounts.get(region)
    if account_id:
        return 'arn:aws:lambda:{}:{}:function:{}-{}'.format(region, account_id, mode.upper(), task)
    else:
        raise Exception('Unrecognized region')


def scale_oversized_images_in_manifest(manifest, bucket=None, key_prefix=None, uri_prefix=None):
    new_manifest = []
    for item in manifest:
        new_item = item.copy()
        img, scalar = scale_image_to_size(uri=new_item['source-ref'])
        if scalar is not None:
            if uri_prefix:
                (bucket, key_prefix) = s3.decompose_uri(uri_prefix)
            if key_prefix is None:
                key_prefix = 'labeling_temp_images/'
            uri = s3.write_temp_object(img, key_prefix, bucket=bucket)
            new_item['original-source-ref'] = new_item.pop('source-ref')
            new_item['source-ref'] = uri
            new_item['scalar'] = scalar
        new_manifest.append(new_item)
    return new_manifest


def reverse_scaling_of_annotation(manifest, label_attribute_name, delete_scaled_images=True):
    new_manifest = []
    for item in manifest:
        new_item = item.copy()
        if 'scalar' in new_item:
            source_image = new_item.pop('old-source-ref')
            scalar = new_item.pop('scalar')
            scaled_image = new_item['source-ref']
            if delete_scaled_images:
                s3.delete(uri=scaled_image)
            new_item['source-ref'] = source_image
            for annotation in new_item[label_attribute_name]['annotations']:
                annotation['width'] = int(annotation['width'] / scalar)
                annotation['height'] = int(annotation['height'] / scalar)
                annotation['top'] = int(annotation['top'] / scalar)
                annotation['left'] = int(annotation['left'] / scalar)
        new_manifest.append(new_item)
    return new_manifest
