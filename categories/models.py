from django.db import models
from config.model_utils.models import TimeStampedModel
from config.utils.image_validators import validate_image_size, validate_image_resolution


class Category(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('products.Product', related_name='categories')

    

class CategoryImage(TimeStampedModel, models.Model):
    image = models.ImageField(upload_to='categories/', validators=[validate_image_size, validate_image_resolution])
    category = models.ForeignKey('categories.Category', related_name='images', on_delete=models.CASCADE)
    
        

