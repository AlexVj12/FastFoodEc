from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Local(models.Model):
    nombre = models.CharField(max_length = 250, unique=True)
    imagen = models.CharField(max_length = 250)
    puntaje= models.FloatField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    costoEnvio = models.FloatField()
    descripcion = models.CharField(max_length=150)
    tiempo_entrega = models.CharField(max_length=50)
    direccion = models.CharField(max_length=250)
       
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length = 20)
    descripcion= models.CharField(max_length = 150)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} : {self.local.nombre}'


class Producto(models.Model):
    nombre = models.CharField(max_length = 100)
    imagen = models.CharField(max_length = 250)
    descripcion= models.CharField(max_length = 150)
    precio =models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} : {self.categoria.nombre}'


class Persona(models.Model):
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=10)
    ciudad = models.CharField(max_length = 100)
    direccion = models.CharField(max_length=250)
    class Meta:
        abstract = True


class Cliente(Persona):
    imagen = models.CharField(max_length = 250)
    usuario = models.OneToOneField(User,on_delete= models.CASCADE)
    
    def __str__(self):
        return f'Cuenta de {self.usuario.username}'


class Pedido(models.Model):
    fecha_pedido = models.DateTimeField()
    total = models.FloatField()
    producto = models.ManyToManyField(Producto)
    direccion = models.CharField(max_length = 250)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    
