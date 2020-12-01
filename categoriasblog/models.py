from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ['-created']

    def __str__(self):
        return self.name