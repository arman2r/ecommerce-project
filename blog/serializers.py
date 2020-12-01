from rest_framework import serializers
from blog.models import Post
from django.utils.html import strip_tags

class PostSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    def get_categories(self, obj): 
         return obj.categories.name
    
    def get_author(self, obj): 
         return obj.author.first_name
     
    class Meta:
        model = Post
        fields = '__all__'
        
        def to_representation(self, instance):
          data = super().to_representation(instance)
          data['content'] = strip_tags(instance.content)
          return data
        
     