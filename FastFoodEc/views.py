from datetime import datetime
import datetime
from math import prod
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from multiprocessing import context
import re
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from FastFoodEc.Carrito import Carrito
from FastFoodEc.context_processor import total_carrito
from .models import *
from .forms import *

def index_view(request):
    return render(request,"index.html")

@login_required(login_url = 'login')
def admin_view(request):
    locales = Local.objects.all()
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    
    context = {
        'locales':locales,
        'categorias':categorias,
        'productos':productos
    }

    return render(request,"./admin/admin.html",context)

@login_required(login_url = 'login')
def local_view(request):
    locales = Local.objects.all()
    formCategoria = categoria_form

    if request.method == "POST":
        formCategoria = categoria_form(request.POST)
        if formCategoria.is_valid():
            
            Categoria.objects.create(**formCategoria.cleaned_data)
    context = {
        'locales':locales,
    }

    return render(request,"./local/local.html",context)
    
@login_required(login_url = 'login')
def agregar_local_view(request):
    form = Local_form
   
    context ={
        'form':form,
    }

    return render(request,"local/agregar.html",context)

@login_required(login_url = 'login')
def agregar_local_categorias(request):
    form = Local_form
    formCategoria = categoria_form
    if request.method == "POST":
        form = Local_form(request.POST)
        if form.is_valid():
            
            Local.objects.create(**form.cleaned_data)
    
    context ={
        'formCategoria':formCategoria
    }


    return render(request,"local/agregar_categoria.html",context)


@login_required(login_url = 'login')
def view_local(request,id):
    local = Local.objects.get(id=id)
    categorias =Categoria.objects.get(local_id = id)
    context={
        'local':local,
        'categorias':categorias
    }
    return render(request,"local/view.html",context)

@login_required(login_url = 'login')
def eliminar_Local(request, id):
  local = Local.objects.get(id=id)
  local.delete()
  return HttpResponseRedirect(reverse('local'))
   

def register_user(request):
    formC = cliente_form
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.save()
           
            dataU ={
                "idUser":data.id,
                "formC":formC
            }
            return render(request,'user/register-complete.html',dataU)

    else:
        form = UserRegisterForm()

    if request.method == 'POST':
        formC = cliente_form(request.POST)
        if formC.is_valid():
            cliente = Cliente()
            user = User.objects.get(id =request.POST['usuario_id'])
            cliente.imagen= formC.cleaned_data['imagen']
            cliente.nombres = formC.cleaned_data['nombres']
            cliente.apellidos= formC.cleaned_data['apellidos']
            cliente.telefono= formC.cleaned_data['telefono']
            cliente.ciudad = formC.cleaned_data['ciudad']
            cliente.direccion = formC.cleaned_data['direccion']
            cliente.usuario = user
            cliente.save()
            return HttpResponseRedirect(reverse('login'))


    context={
        'form':form
    }

    return render(request,"user/register.html",context)


@login_required(login_url = 'login')
def delivery_view(request):
    user = request.user
    locales = Local.objects.all()
    cliente = Cliente.objects.get(usuario_id=user.id)
    context = {
        'locales':locales,
        'cliente':cliente
      
    }
    
    return render(request,"delivery/delivery.html",context)

@login_required(login_url = 'login')
def profile(request,usuarioID):
    formC = cliente_form
    user = request.user
    cliente = Cliente.objects.get(usuario_id=usuarioID)
    pedidos =  Pedido.objects.order_by('-fecha_pedido').filter(user_id=user.id)



    context = {
        'cliente':cliente,
        'pedidos':pedidos,
        'formC':formC,

    }
    
    return render(request,"delivery/profile.html",context)

@login_required(login_url = 'login')
def local_detail(request,id):

    local = Local.objects.get(id=id)
    categorias = Categoria.objects.order_by('nombre').filter(local_id=id)
    idsCategorias = Categoria.objects.filter(local_id=id).values_list('id', flat=True)
    productos =  Producto.objects.order_by('nombre').filter(categoria_id__in=idsCategorias)
    user = request.user
    cliente = Cliente.objects.get(usuario_id=user.id)

    context={
        "local":local,
        "categorias":categorias,
        "productos":productos,
        'cliente':cliente
    }

    return render(request,"delivery/local_detail.html",context)

@login_required(login_url = 'login')
def mostrarCategoria(request,idlocal,idCategoria):
    local = Local.objects.get(id=idlocal)
    categoria = Categoria.objects.get(id=idCategoria)
    productos =  Producto.objects.order_by('nombre').filter(categoria_id=idCategoria)
    categorias = Categoria.objects.order_by('nombre').filter(local_id=idlocal)
    user = request.user
    cliente = Cliente.objects.get(usuario_id=user.id)

    
    context = {
        "productosC":productos,
        'cliente':cliente,
        "local":local,
        "categoriaN":categoria,
        "categorias":categorias
    }

    return render(request,"delivery/categoria.html",context)

@login_required(login_url = 'login')
def carrito(request):
    user = request.user
    cliente = Cliente.objects.get(usuario_id=user.id)
    context = {
        
        'cliente':cliente
      
    }
    
    return render(request,"delivery/carrito.html",context)

@login_required(login_url = 'login')
def agregarPedido(request):
    productos = []

    user = request.user
    usuario = User.objects.get(id=user.id)
    cliente = Cliente.objects.get(usuario_id =user.id)
    fecha = datetime.datetime.now()
    fechaFormato = fecha.strftime("%Y-%m-%d %H:%M:%S")


    total = total_carrito(request)
    print(cliente)
    print(total['total_carrito'])
    carrito = Carrito(request) 

    pedido = Pedido.objects.create(fecha_pedido = fechaFormato, total = total['total_carrito'], direccion = cliente.direccion, user = usuario)
    
    for key, value in carrito.carrito.items():
        producto = Producto.objects.get(id=value["producto_id"])
        productos.append(producto)
        print(f'{value["producto_id"]} : {value["nombre"]}')

    pedido.producto.set(productos)
    
    carrito.vaciar_carrito()
    return redirect('delivery_view')

@login_required(login_url = 'login')

def agregar_producto(request, producto_id):

    idCategoria = Producto.objects.filter(id=producto_id).values_list('categoria_id', flat=True)
    idLocal = Categoria.objects.filter(id=idCategoria[0]).values_list('local_id', flat=True)
   
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar_producto(producto)

    return redirect("local_detail",id=idLocal[0])


@login_required(login_url = 'login')
def eliminar_producto(request, producto_id):
    idCategoria = Producto.objects.filter(id=producto_id).values_list('categoria_id', flat=True)
    idLocal = Categoria.objects.filter(id=idCategoria[0]).values_list('local_id', flat=True)
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar_producto(producto)
    
    return redirect("local_detail",id=idLocal[0])

@login_required(login_url = 'login')

def disminuir_producto(request, producto_id):
    idCategoria = Producto.objects.filter(id=producto_id).values_list('categoria_id', flat=True)
    idLocal = Categoria.objects.filter(id=idCategoria[0]).values_list('local_id', flat=True)
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.disminuir_producto(producto)
    return redirect("local_detail",id=idLocal[0])



@login_required(login_url = 'login')
def vaciar_carrito(request):
    carrito = Carrito(request)
    carrito.vaciar_carrito()
    return redirect("delivery_view",)


def actualizar_cliente(request,idCliente):
    user = request.user
    cliente = Cliente.objects.get(id=idCliente)
    print(cliente.nombres)
    cliente.imagen= request.POST['imagen']
    cliente.nombres = request.POST['nombres']
    cliente.apellidos= request.POST['apellidos']
    cliente.telefono= request.POST['telefono']
    cliente.ciudad = request.POST['ciudad']
    cliente.direccion = request.POST['direccion']
    cliente.save()
    
    return redirect("account",usuarioID=user.id)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        cliente = Cliente.objects.get(usuario_id=token.user_id)
        return Response({'token': token.key, 'id': token.user_id, 'Cliente': cliente.id} ) 

 