from django.db import models
from django.core.validators import MaxValueValidator
from config.model_utils.models import TimeStampedModel
from products.choices import Currency
from users.models import User
from config.utils.image_validators import validate_image_size, validate_image_resolution, validate_image_count

class Product(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    tags = models.ManyToManyField("products.ProductTag", related_name='products', blank=True)
    quantity = models.PositiveIntegerField()

    def average_rating(self):
        pass

    
    def __str__(self):
        return f'name : {self.name}, price : {self.price}{dict(Currency.choices).get(self.currency, self.currency)}'
    





class Review(TimeStampedModel, models.Model):
    product = models.ForeignKey('products.Product', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    
    def __str__(self):
        return f"review by : {self.user.username}"
    
    


class FavoriteProduct(TimeStampedModel, models.Model):
    product = models.ForeignKey('products.Product', related_name='favorite_products', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='favorite_products', on_delete=models.SET_NULL, null=True, blank=True)




class ProductTag(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name




class Cart(TimeStampedModel, models.Model):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.SET_NULL, null=True, blank=True)



class CartItem(TimeStampedModel, models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_of_addition = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} items'
    
    def total_price(self):
        return self.quantity * self.price_at_time_of_addition


class ProductImage(TimeStampedModel, models.Model):
    image = models.ImageField(upload_to='products/', validators=[validate_image_size, validate_image_resolution])
    product = models.ForeignKey('products.Product', related_name='images', on_delete=models.CASCADE)
    
    def clean(self):
        if self.product_id:
            validate_image_count(self.product_id)
        super().clean()
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        