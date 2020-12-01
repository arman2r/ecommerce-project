from django.shortcuts import render
from categoriasblog.models import Category as CategoryModel
from rest_framework.permissions import AllowAny
from rest_framework.views import  APIView
from rest_framework.response import Response
from categoriasblog.serializers import CategorySerializer

# Create your views here.

class Category(APIView):
    
    permission_classes = (AllowAny,)
    
    def get(self, request):        
        queryset = CategoryModel.objects.all()
        serializer = CategorySerializer(queryset, many=True)
    
        return Response(serializer.data)