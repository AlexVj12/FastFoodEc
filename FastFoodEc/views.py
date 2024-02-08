from datetime import datetime
import datetime
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from FastFoodEc.Carrito import Carrito
from FastFoodEc.context_processor import total_carrito
from .models import Local,Categoria,Producto,Cliente,Pedido
from .forms import local_form,categoria_form,cliente_form,UserRegisterForm
from django.views.decorators.http import require_http_methods,require_safe

@require_safe
def index_view(request):
    return render(request,"index.html")

@login_required(login_url='login')
@require_safe
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

@login_required(login_url='login')
@require_safe
def local_view(request):
    locales = Local.objects.all()

    if request.method == "POST":
        form_categoria = categoria_form(request.POST)
        if form_categoria.is_valid():
            Categoria.objects.create(**form_categoria.cleaned_data)
    context = {
        'locales':locales,
    }

    return render(request,"./local/local.html",context)
    
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def agregar_local_view(request):
    form = local_form
   
    context ={
        'form':form,
    }

    return render(request,"local/agregar.html",context)

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def agregar_local_categorias(request):

    form_categoria = categoria_form
    if request.method == "POST":
        form = local_form(request.POST)
        if form.is_valid():
            Local.objects.create(**form.cleaned_data)
    
    context ={
        'formCategoria':form_categoria
    }

    return render(request,"local/agregar_categoria.html",context)


@login_required(login_url='login')
@require_safe
def view_local(request,id):
    local = Local.objects.get(id=id)
    categorias =Categoria.objects.get(local_id=id)
    context={
        'local':local,
        'categorias':categorias
    }
    return render(request,"local/view.html",context)

@require_http_methods(["POST" ,"GET"])
def register_user(request):
    form_cliente = cliente_form
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.save()
           
            data_user ={
                'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
                "idUser":data.id,
                "formC":form_cliente
            }
            return render(request,'user/register-complete.html',data_user)

    else:
        form = UserRegisterForm()

    if request.method == 'POST':
        form_cliente = cliente_form(request.POST)
        if form_cliente.is_valid():
            cliente = Cliente()
            user = User.objects.get(id =request.POST['usuario_id'])
            cliente.imagen= form_cliente.cleaned_data['imagen']
            cliente.nombres = form_cliente.cleaned_data['nombres']
            cliente.apellidos= form_cliente.cleaned_data['apellidos']
            cliente.telefono= form_cliente.cleaned_data['telefono']
            cliente.ciudad = form_cliente.cleaned_data['ciudad']
            cliente.direccion = form_cliente.cleaned_data['direccion']
            cliente.usuario = user
            cliente.save()
            return HttpResponseRedirect(reverse('login'))


    context={
        'form':form
    }

    return render(request,"user/register.html",context)


@login_required(login_url='login')
@require_safe
def delivery_view(request):
    user = request.user
    locales = Local.objects.all()
    cliente = Cliente.objects.get(usuario_id=user.id)
    context = {
        'locales':locales,
        'cliente':cliente
      
    }
    
    return render(request,"delivery/delivery.html",context)

@login_required(login_url='login')
@require_safe
def profile(request,usuario_id):
    form_cliente = cliente_form
    user = request.user
    cliente = Cliente.objects.get(usuario_id=usuario_id)
    pedidos =  Pedido.objects.order_by('-fecha_pedido').filter(user_id=user.id)

    context = {
        'cliente':cliente,
        'pedidos':pedidos,
        'form':form_cliente,
    }
    
    return render(request,"delivery/profile.html",context)

@login_required(login_url='login')
@require_safe
def local_detail(request,id_local):
    local = Local.objects.get(id=id_local)

    categorias = Categoria.objects.order_by('nombre').filter(local_id=id_local)
    ids_categorias = Categoria.objects.filter(local_id=id_local).values_list('id', flat=True)
    productos =  Producto.objects.order_by('nombre').filter(categoria_id__in=ids_categorias)
    user = request.user
    cliente = Cliente.objects.get(usuario_id=user.id)

    context={
        "local":local,
        "categorias":categorias,
        "productos":productos,
        'cliente':cliente
    }

    return render(request,"delivery/local_detail.html",context)

@login_required(login_url='login')
@require_safe
def mostrar_categoria(request,id_local,id_categoria):
    local = Local.objects.get(id=id_local)
    categoria = Categoria.objects.get(id=id_categoria)
    productos =  Producto.objects.order_by('nombre').filter(categoria_id=id_categoria)
    categorias = Categoria.objects.order_by('nombre').filter(local_id=id_local)
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

@login_required(login_url='login')
@require_safe
def carrito(request):
    user = request.user
    cliente = Cliente.objects.get(usuario_id=user.id)
    context = {
        'cliente':cliente
    }
    
    return render(request,"delivery/carrito.html",context)

@login_required(login_url='login')
@require_http_methods(["GET"])
def agregar_pedido(request):
    productos = []

    user = request.user
    usuario = User.objects.get(id=user.id)
    cliente = Cliente.objects.get(usuario_id=user.id)
    fecha = datetime.datetime.now()
    fecha_formato = fecha.strftime("%Y-%m-%d %H:%M:%S")

    total = total_carrito(request)
    print(cliente)
    print(total['total_carrito'])
    carrito = Carrito(request) 

    pedido = Pedido.objects.create(fecha_pedido = fecha_formato, total = total['total_carrito'], direccion = cliente.direccion, user = usuario)
    
    for key, value in carrito.carrito_session.items():  # Aquí se hace el cambio
        producto = Producto.objects.get(id=value["producto_id"])
        productos.append(producto)
        print(f'{value["producto_id"]} : {value["nombre"]}')

    pedido.producto.set(productos)
    
    carrito.vaciar_carrito()
    return redirect('delivery_view')


@login_required(login_url='login')
@require_http_methods(["POST", "GET"])
def agregar_producto(request, producto_id):

    id_categoria = Producto.objects.filter(id=producto_id).values_list('categoria_id', flat=True)
    local_id = Categoria.objects.filter(id=id_categoria[0]).values_list('local_id', flat=True)
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar_producto(producto)

    return redirect("local_detail",id_local=local_id[0])


@login_required(login_url='login')
@require_http_methods(["POST"])
def eliminar_producto(request, producto_id):
    id_categoria = Producto.objects.filter(id=producto_id).values_list('categoria_id', flat=True)
    id_local = Categoria.objects.filter(id=id_categoria[0]).values_list('local_id', flat=True)
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar_producto(producto)
    
    return redirect("local_detail",id=id_local[0])

@login_required(login_url='login')
@require_http_methods(["POST","GET"])
def disminuir_producto(request, producto_id):
    id_categoria = Producto.objects.filter(id=producto_id).values_list('categoria_id', flat=True)
    id_local = Categoria.objects.filter(id=id_categoria[0]).values_list('local_id', flat=True)
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.disminuir_producto(producto)
    return redirect("local_detail",id_local=id_local[0])

@login_required(login_url='login')

@require_http_methods(["POST","GET"])
def vaciar_carrito(request):
    carrito = Carrito(request)
    carrito.vaciar_carrito()
    return redirect("delivery_view",)

@login_required(login_url='login')
@require_http_methods(["POST"])
def actualizar_cliente(request,id_cliente):
    user = request.user
    cliente = Cliente.objects.get(id=id_cliente)
    print(cliente.nombres)
    cliente.imagen= request.POST['imagen']
    cliente.nombres = request.POST['nombres']
    cliente.apellidos= request.POST['apellidos']
    cliente.telefono= request.POST['telefono']
    cliente.ciudad = request.POST['ciudad']
    cliente.direccion = request.POST['direccion']
    cliente.save()
    
    return redirect("account",usuario_id=user.id)

class CustomObtainAuthToken(ObtainAuthToken):
    @require_http_methods(["POST"])
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        cliente = Cliente.objects.get(usuario_id=token.user_id)
        return Response({'token': token.key, 'id': token.user_id, 'Cliente': cliente.id})
