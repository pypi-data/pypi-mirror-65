import math
from io import BytesIO
import collections
from larry import s3


def scale_image_to_size(image=None, bucket=None, key=None, uri=None, max_pixels=None, max_bytes=None):
    try:
        from PIL import Image
        if image:
            src_bytes = _image_byte_count(image)
        else:
            src_bytes = s3.get_object_size(bucket, key, uri)
            image = s3.read_pillow_image(bucket, key, uri)
        x, y = image.size
        src_pixels = x * y
        bytes_scalar = math.sqrt(max_bytes/src_bytes) if max_bytes else 1
        pixels_scalar = math.sqrt(max_pixels/src_pixels) if max_pixels else 1
        scalar = min(bytes_scalar, pixels_scalar)
        if scalar >= 1:
            return image, None
        else:
            new_x = int(scalar * x)
            new_y = int(scalar * y)
            new_image, scalar = image.resize((new_x, new_y), Image.BICUBIC), scalar
            if max_bytes and _image_byte_count(new_image) > max_bytes:
                return scale_image_to_size(image=image, max_pixels=max_pixels, max_bytes=int(max_bytes*0.95))
            else:
                return new_image, scalar
    except ImportError as e:
        # Simply raise the ImportError to let the user know this requires Pillow to function
        raise e


def _image_byte_count(image):
    buff = BytesIO()
    image.save(buff, 'PNG' if image.format is None else image.format)
    return len(buff.getvalue())


def annotation_to_coordinates(box):
    return [box['left'], box['top'], box['left']+box['width']-1, box['top']+box['height']-1]


def box_coordinates(box):
    coords = box.get('coordinates')
    if coords:
        return coords
    else:
        return annotation_to_coordinates(box)


def scale_box(box, scalar):
    bbox = augment_box_attributes(box.copy())
    bbox['left'] = box['left'] * scalar
    bbox['top'] = box['top'] * scalar
    bbox['width'] = box['width'] * scalar
    bbox['height'] = box['height'] * scalar
    bbox['coordinates'] = annotation_to_coordinates(bbox)
    return bbox


def augment_box_attributes(box):
    if 'coordinates' not in box and 'top' in box and 'left' in box and 'width' in box and 'height' in box:
        box['coordinates'] = annotation_to_coordinates(box)
    elif 'coordinates' in box and ('top' not in box or 'left' not in box):
        box['left'] = box['coordinates'][0]
        box['top'] = box['coordinates'][1]
        box['width'] = box['coordinates'][2] - box['coordinates'][0] + 1
        box['height'] = box['coordinates'][3] - box['coordinates'][1] + 1
    return box


def box_area(box):
    if isinstance(box, collections.Mapping):
        box = box_coordinates(box)
    if box:
        return (box[2] - box[0]) * (box[3] - box[1])
    else:
        return 0


def box_intersection(a, b):
    if isinstance(a, collections.Mapping):
        a = box_coordinates(a)
    if isinstance(b, collections.Mapping):
        b = box_coordinates(b)
    intersection = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    if intersection[2] < intersection[0] or intersection[3] < intersection[1]:
        return None
    else:
        return intersection


def intersection_over_union(a, b):
    ac = box_coordinates(a)
    bc = box_coordinates(b)
    intersection = box_area(box_intersection(ac, bc))
    union = box_area(ac) + box_area(bc) - intersection
    return intersection / union


def render_boxes(boxes,
                 image=None,
                 image_uri=None,
                 color=None,
                 width=None,
                 label_size=None,
                 label=None,
                 annotation_filter=None,
                 get_box=None,
                 color_index=None):
    if image_uri:
        image = s3.read_pillow_image(uri=image_uri)
    # Change palette mode images to RGB so that standard palette colors can be drawn on them
    if image.mode == 'P':
        image = image.convert(mode='RGB')
    else:
        image = image.copy()
    if color is None:
        color = get_color_list()
    width = round(image.width / 512) + 1 if width is None else width
    label_size = 20 if label_size is None else label_size

    try:
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)

        # TODO Find a better way to pull in fonts
        font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", size=label_size)

        for idx, item in enumerate(boxes):
            if annotation_filter is None or annotation_filter(idx, item):

                # Retrieve the box coordinates from the annotation
                if get_box:
                    item = get_box(idx, item)
                box = box_coordinates(item)

                # select a color to use with this box
                if isinstance(color, str):
                    box_color = color
                elif callable(color):
                    box_color = color(idx, item)
                elif color_index:
                    # TODO: Fix array out of bounds issue
                    box_color = color[color_index(idx, item)]
                else:
                    box_color = 'green'
                draw.rectangle(box, outline=box_color, width=width)
                if label:
                    if isinstance(label, str):
                        text = label
                    else:
                        text = label(idx, item)
                    size = draw.textsize(text,
                                         font=font,
                                         spacing=0)
                    draw.multiline_text((box[0] - size[0] - 4, box[1] + 4),
                                        text,
                                        fill=box_color,
                                        font=font,
                                        spacing=0,
                                        align='right')
        return image
    except ImportError as e:
        # Simply raise the ImportError to let the user know this requires Pillow to function
        raise e


def get_color_list():
    return [(44, 160, 44), (31, 119, 180), (255, 127, 14), (214, 39, 40), (148, 103, 189), (140, 86, 75),
            (227, 119, 194), (127, 127, 127), (188, 189, 34), (255, 152, 150), (23, 190, 207),
            (174, 199, 232), (255, 187, 120), (152, 223, 138), (197, 176, 213)]


def generate_label(keys):
    key_list = keys

    def gen_label(idx, item):
        label = ''
        for key in key_list:
            if len(label) != 0:
                label = label + '\n'
            if key == 'index':
                label = label + item.get(key, idx)
            else:
                label = item.get(key)
        return label


# TODO: Add image_url parameter
def render_bounding_box_assignments(assignments,
                                    image=None,
                                    image_uri=None,
                                    labels=None,
                                    single_image=True):
    return render_boxes_from_objects(assignments,
                                     lambda item: item['Answer']['boundingBox']['boundingBoxes'],
                                     image,
                                     image_uri,
                                     labels,
                                     single_image)


def render_boxes_from_objects(objects,
                              accessor,
                              image=None,
                              image_uri=None,
                              labels=None,
                              single_image=True,
                              color=None):
    # TODO: Avoid an unnecessary copy step when coming from uri
    if image_uri:
        image = s3.read_pillow_image(uri=image_uri)
    # Change palette mode images to RGB so that standard palette colors can be drawn on them
    if image.mode == 'P':
        image = image.convert(mode='RGB')
    else:
        image = image.copy()

    if isinstance(objects, collections.Mapping):
        annotation = accessor(objects)
        if labels:
            return render_boxes(annotation, image=image, image_uri=image_uri, color=color,
                                color_index=lambda idx, item: _find_label_index(item, labels))
        else:
            return render_boxes(annotation, image=image, image_uri=image_uri, color=color)
    elif single_image:
        for idx, obj in enumerate(objects):
            annotation = accessor(obj)
            if callable(color):
                image = render_boxes(annotation, image=image,
                                     color=lambda o_idx, e_idx, item: color(idx, e_idx, item),
                                     color_index=lambda i, item: idx)
            else:
                image = render_boxes(annotation, image=image,
                                     color_index=lambda i, item: idx)
        return image
    else:
        images = []
        for idx, obj in enumerate(objects):
            annotation = accessor(obj)
            if callable(color):
                images.append(render_boxes(annotation, image=image,
                                           color=lambda e_idx, item: color(idx, e_idx, item),
                                           color_index=lambda i, item: idx))
            else:
                images.append(render_boxes(annotation, image=image,
                                           color_index=lambda i, item: idx))
        return images


def _find_label_index(item, labels):
    if 'label' in item:
        for idx, label in enumerate(labels):
            if label == item['label']:
                return idx
    else:
        return 0


def tile_images(images, max_width=3000):
    try:
        from PIL import Image

        # TODO: Add handling for variably sized images?
        (x, y) = images[0].size
        columns = min(max(math.floor(max_width / x), 1), len(images))
        rows = math.ceil(len(images) / columns)
        canvas = Image.new('RGB', (x * columns, y * rows), color='white')

        for idx, image in enumerate(images):
            row = math.floor(idx / columns)
            column = idx - (row * columns)
            canvas.paste(image, (column * x, row * y))
        return canvas
    except ImportError as e:
        # Simply raise the ImportError to let the user know this requires Pillow to function
        raise e


def join_images(images, horizontal=True):
    try:
        from PIL import Image

        width = 0
        height = 0
        indices = []

        if horizontal:
            for image in images:
                (x, y) = image.size
                height = max(height, y)
                indices.append(width)
                width += x
            indices = [(x, 0) for x in indices]
        else:
            for image in images:
                (x, y) = image.size
                width = max(width, x)
                indices.append(height)
                height += y
            indices = [(0, y) for y in indices]

        canvas = Image.new('RGB', (width, height), color='white')
        for idx, image in enumerate(images):
            canvas.paste(image, indices[idx])

        return canvas, indices
    except ImportError as e:
        # Simply raise the ImportError to let the user know this requires Pillow to function
        raise e
