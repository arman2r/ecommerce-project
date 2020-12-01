from django.urls import path
from blog.views import *


urlpatterns = [
    path('bloger/', Post.as_view()),
    path('filter/<title>/', Posttitle.as_view()),
    path('categorias/<categories>/', Postcategoria.as_view()),
]