from django.shortcuts import render
from blog.models import Post as PostModel
from rest_framework.permissions import AllowAny
from rest_framework.views import  APIView
from rest_framework.response import Response
from blog.serializers import PostSerializer

# Create your views here.

class Post(APIView):
    
    permission_classes = (AllowAny,)
    
    def get(self, request):        
        queryset = PostModel.objects.all()
        serializer = PostSerializer(queryset, many=True)
    
        return Response(serializer.data)
    
class Posttitle(APIView):
    
    permission_classes = (AllowAny,)
    
    def get(self, request, title):        
        queryset = PostModel.objects.all().filter(title=title)
        serializer = PostSerializer(queryset, many=True)
    
        return Response(serializer.data)
    
class Postcategoria(APIView):
    
    permission_classes = (AllowAny,)
    
    def get(self, request, categories):        
        queryset = PostModel.objects.all().filter(categories=categories)
        serializer = PostSerializer(queryset, many=True)
    
        return Response(serializer.data)