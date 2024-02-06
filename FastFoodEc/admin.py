from multiprocessing.connection import Client
from django.contrib import admin

from. models import *


admin.site.register(Local)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Pedido)