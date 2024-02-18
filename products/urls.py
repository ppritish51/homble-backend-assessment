from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import products_list, SkuViewSet, ProductDetailView

router = DefaultRouter()
router.register(r'skus', SkuViewSet)
router.register(r'products', ProductDetailView)

urlpatterns = [
    path("list/", products_list, name='products-list'),
    path('api/', include(router.urls)),
]
