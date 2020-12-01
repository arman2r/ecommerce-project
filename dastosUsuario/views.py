from django.shortcuts import render
from dastosUsuario.models import Datos as DatosModel
from dastosUsuario.serializers import DatosSerializer
from rest_framework.views import  APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import generics

# Create your views here.

#class DatosListView(generics.ListAPIView):
 #   permission_classes = (AllowAny,)
  #  queryset = DatosModel.objects.filter(usuario__id=id)
   # serializer_class = DatosSerializer 
class Datospost(APIView):
    #permission_classes = (AllowAny,)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):        
        queryset = DatosModel.objects.all()
        serializer = DatosSerializer(queryset, many=True)
    
        return Response(serializer.data)
    
    def post(self,request):
        serializer = DatosSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Datos(APIView):
    #permission_classes = (AllowAny,)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        queryset = DatosModel.objects.filter(usuario__id=id)            
        serializer = DatosSerializer(queryset, many=True)
    
        return Response(serializer.data)


   
@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Datos_detail(request,id):
    
        try:
            datos = DatosModel.objects.get(id=id)
        except DatosModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = DatosSerializer(datos)
            return Response(serializer.data)
        

        elif request.method == 'PUT':
            serializer = DatosSerializer(datos, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)