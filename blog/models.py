from django.db import models
from django.conf import settings
from django.utils.timezone import now
from categoriasblog.models import Category
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    content = RichTextField(verbose_name="Contenido")
    published = models.DateTimeField(verbose_name="Fecha de publicación", default=now)
    video = models.CharField(verbose_name="Video", null=True, blank=True, max_length=50)
    image = models.ImageField(verbose_name="Imagen", upload_to="blog", null=True, blank=True)
    image_banner = models.ImageField(verbose_name="Imagen banner", upload_to="blog", null=True, blank=True)
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, verbose_name="Categorías", related_name="categories", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "entrada"
        verbose_name_plural = "entradas"
        ordering = ['-created']

    def __str__(self):
        return self.title
