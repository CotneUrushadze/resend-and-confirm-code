from django.urls import path, include
from categories.views import CategoryImageViewSet, CategoryListView, CategoryDetailView
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('categories', CategoryListView, basename='category-list')
router.register('detail', CategoryDetailView, basename='category-detail')  

products_router = routers.NestedDefaultRouter(
    router,
    'categories',
    lookup = 'category'
)
products_router.register('images', CategoryImageViewSet, basename='category-images')




urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),

    # path('categories/', CategoryListView.as_view({'get': 'list'}), name='category-list'),
    # path('categories/<int:pk>', CategoryDetailView.as_view({'get': 'retrieve'}), name='category-detail'),
    # path('categories/<int:category_id>/images/', CategoryImageViewSet.as_view({'get': 'list', 'post':'create'}), name='category-images'),
]
