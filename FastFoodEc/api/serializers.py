
from rest_framework import serializers
from FastFoodEc.models import *
from django.contrib.auth.models import User

class LocalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'

class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = 'username','password','email'
        

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class PedidoSerializer(serializers.HyperlinkedModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    id = serializers.ReadOnlyField()
    #producto = ProductoSerializer(many=True, read_only=True)
    class Meta:
        model = Pedido
        fields = '__all__'


