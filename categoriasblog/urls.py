from django.urls import path
from categoriasblog.views import Category


urlpatterns = [
    path('categorias/', Category.as_view()),
]