
import imp
from re import template
from django.contrib import admin
from rest_framework import routers
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from rest_framework.authtoken.views import obtain_auth_token  
from FastFoodEc.views import *
from FastFoodEc.api.api import *





router = routers.DefaultRouter()
router.register(r'Local', LocalAPIView)
router.register(r'Categoria', CategoriaAPIView)
router.register(r'Producto', ProductoAPIView)
router.register(r'User', UserAPIView)
router.register(r'Cliente', ClienteAPIView)
router.register(r'Pedido', PedidoAPIView)



urlpatterns = [
    path('',index_view,name = 'index'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', CustomObtainAuthToken.as_view()),
    #path('test_auth/', TestAuthView.as_view(), name='test_auth', ),
    #path('admin/login',LoginView.as_view(),name = 'login'),
    #path('admin/local/logout',LogoutView.as_view(),name = 'logout'),
    #path('admin/',admin_view,name = 'admin'),
    #path('admin/local/',local_view,name = 'local'),
    #path('admin/local/agregar',agregar_local_view,name = 'agregar_local'),
    #path('admin/local/agregar_categorias',agregar_local_categorias,name = 'agregar_local_categorias'),
    #path('admin/local/view/<int:id>',view_local,name = 'view_local'),
    #path('admin/local/eliminar/<int:id>',eliminar_Local,name = 'eliminar_local'),

    path('delivery/',delivery_view,name = 'delivery_view'),
    path('delivery/detail/<int:id>',local_detail,name = 'local_detail'),
    path('login/',LoginView.as_view(template_name = 'user/login.html'),name = 'login'),
    path('logout/',LogoutView.as_view(),name = 'logout'),
    path('register/',register_user,name = 'register'),
    path('pedido/',agregarPedido,name = 'pedido'),
    path('account/<int:usuarioID>',profile,name = 'account'),
    path('update/<int:idCliente>',actualizar_cliente,name = 'actualizarPerfil'),
    path('carrito/',carrito,name = 'carrito'),
    path('add/<int:idproducto>',profile,name = 'add_producto'),
    path('delivery/detail/<int:idlocal>/categoria/<int:idCategoria>',mostrarCategoria,name = 'mostrar_categoria'),
    path('agregar/<int:producto_id>/', agregar_producto, name="agregar_producto"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="eliminar_producto"),
    path('restar/<int:producto_id>/', disminuir_producto, name="disminuir_producto"),
    path('vaciar/', vaciar_carrito, name="vaciar_carrito"),


]
