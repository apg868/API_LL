from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated]   )
def menu_items(request):
    if(request.method=='GET'):
        if(request.user.groups.filter(name='Customer').exists() or request.user.groups.filter(name='Delivery Crew').exists()) or request.user.groups.filter(name='Manager').exists():
            items = MenuItem.objects.select_related('category')
            category_hold = request.query_params.get('category')
            price_hold = request.query_params.get('to_price')
            if category_hold:
                items = items.filter(category__title=category_hold)
            if price_hold:
                items = items.filter(price__lte=price_hold)
            serializedReturn = MenuItemSerializer(items, many=True)
            serializedReturnData = serializedReturn.data
            return Response(serializedReturnData)
        else:
            return Response({'message': 'You do not have the required permissions.'}, status=status.HTTP_403_FORBIDDEN)

    return Response({'message': 'Unsupported method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def menu_item
