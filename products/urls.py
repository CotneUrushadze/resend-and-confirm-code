from django.urls import path, include
from products.views import ReviewViewSet, ProductViewSet, FavoriteProductViewSet, CartViewSet, ProductTagViewSet, ProductImageViewSet, CartItemViewSet
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('cart', CartViewSet)
router.register('favorite_products', FavoriteProductViewSet)
router.register('tags', ProductTagViewSet)
router.register('cart-items', CartItemViewSet, basename = 'cart-items')


products_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup = 'product'
)
products_router.register('images', ProductImageViewSet, basename='product-images')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')






urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),    
]