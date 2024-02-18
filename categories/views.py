from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from categories.models import Category
from categories.serializers import CategorySerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def category_list(request):
    """
    View to list all categories with nested products.
    Only accessible by admin/staff users.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
