from django.contrib import admin
from rest_framework import routers
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from rest_framework.authtoken.views import obtain_auth_token  
from FastFoodEc.views import CustomObtainAuthToken,index_view,delivery_view,local_detail,register_user,agregar_pedido,profile,actualizar_cliente,carrito,agregar_producto,eliminar_producto,disminuir_producto,vaciar_carrito,mostrar_categoria
from FastFoodEc.api.api import LocalAPIView,CategoriaAPIView,ProductoAPIView,UserAPIView,ClienteAPIView,PedidoAPIView



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
    path('delivery/',delivery_view,name = 'delivery_view'),
    path('login/',LoginView.as_view(template_name = 'user/login.html'),name = 'login'),
    path('delivery/detail/<int:id_local>',local_detail,name = 'local_detail'),
    path('logout/',LogoutView.as_view(),name = 'logout'),
    path('register/',register_user,name = 'register'),
    path('pedido/',agregar_pedido,name = 'pedido'),
    path('account/<int:usuario_id>',profile,name = 'account'),
    path('update/<int:id_cliente>',actualizar_cliente,name = 'actualizarPerfil'),
    path('carrito/',carrito,name = 'carrito'),
    path('add/<int:idproducto>',profile,name = 'add_producto'),
    path('delivery/detail/<int:id_local>/categoria/<int:id_categoria>',mostrar_categoria,name = 'mostrar_categoria'),
    path('agregar/<int:producto_id>/', agregar_producto, name="agregar_producto"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="eliminar_producto"),
    path('restar/<int:producto_id>/', disminuir_producto, name="disminuir_producto"),
    path('vaciar/', vaciar_carrito, name="vaciar_carrito"),


]
