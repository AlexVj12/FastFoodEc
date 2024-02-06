from rest_framework import  viewsets
from FastFoodEc.models import Local,Categoria,Producto,Cliente
from django.contrib.auth.models import User
from FastFoodEc.api.serializers import *
from rest_framework.permissions import AllowAny

class LocalAPIView(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer
    permission_classes = (AllowAny,)

class CategoriaAPIView(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (AllowAny,)

class ProductoAPIView(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ClienteAPIView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (AllowAny,)

class PedidoAPIView(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = (AllowAny,)
   
