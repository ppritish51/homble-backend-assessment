from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
)

from .models import Product, Sku
from .permissions import IsSupervisor
from .serializers import ProductListSerializer, SkuSerializer, ProductSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def products_list(request):
    """
    List of all products or filtered by refrigeration need.
    """

    is_refrigerated = request.query_params.get('is_refrigerated')

    if is_refrigerated is not None:
        is_refrigerated = is_refrigerated.lower() in ['true', '1']
        products = Product.objects.filter(is_refrigerated=is_refrigerated)
    else:
        products = Product.objects.all()

    serializer = ProductListSerializer(products, many=True)
    return Response({"products": serializer.data}, status=HTTP_200_OK)


class SkuViewSet(viewsets.ModelViewSet):
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer
    permission_classes = [IsSupervisor]

    def perform_create(self, serializer):
        serializer.save(status='pending')  # Default status


class ProductDetailView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSupervisor]

    def get_queryset(self):
        return Product.objects.prefetch_related('skus').filter(skus__status='approved')
