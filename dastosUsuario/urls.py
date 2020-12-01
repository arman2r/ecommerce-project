from django.urls import path
from dastosUsuario.views import *


urlpatterns = [
    path('post/',Datospost.as_view()),
    path('<id>/', Datos.as_view()),
    
    #path('post/',datospost_list, name="post"),
    path('update/<id>/',Datos_detail, name="actualizacion")
]
