from django.core.validators import ValidationError
from PIL import Image
from django.apps import apps


def validate_image_size(image):
    size = image.size
    limit = 5
    if size > limit * 1024 * 1024:
        raise ValidationError(f'Image size exceeds {limit}MB limit.')
    
    

def validate_image_resolution(image):
    image = Image.open(image)
    width, height = image.size
    min_width, min_height = 300, 300
    max_width, max_height =4000, 4000
    if width >= max_width or height >= max_height:
        raise ValidationError('Image resolution exceeds 4000x4000.')
    if width <= min_width or height <= min_height:
        raise ValidationError('Image resolution is less than 300x300.')
    
    

def validate_image_count(product_id):
    ProductImage = apps.get_model('products', 'ProductImage')
    limit = 5
    count = ProductImage.objects.filter(product_id=product_id).count()
    if count >= limit:
        raise ValidationError(f'Cannot add more than {limit} images.')