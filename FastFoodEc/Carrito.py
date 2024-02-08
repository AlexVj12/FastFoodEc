class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito_session = self.session.get("carrito") 

        if not carrito_session:  
            self.session["carrito"] = {}
            self.carrito_session = self.session["carrito"]  
        else:
            self.carrito_session = carrito_session  

    def agregar_producto(self, producto):
        id_producto = str(producto.id)
        if id_producto in self.carrito_session:
            self.carrito_session[id_producto]["cantidad"] += 1
            self.carrito_session[id_producto]["total"] += producto.precio
        else:
            self.carrito_session[id_producto] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "total": producto.precio,
                "imagen": producto.imagen,
                "cantidad": 1,
            }
        self.guardar_carrito()

            
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito_session
        self.session.modified = True

    def eliminar_producto(self, producto):
        id_producto = str(producto.id)
        if id_producto in self.carrito_session:
            del self.carrito_session[id_producto]
            self.guardar_carrito()

    def disminuir_producto(self, producto):
        id_producto = str(producto.id)
        if id_producto in self.carrito_session:
            self.carrito_session[id_producto]["cantidad"] -= 1
            self.carrito_session[id_producto]["total"] -= producto.precio
            if self.carrito_session[id_producto]["cantidad"] <= 0:
                self.eliminar_producto(producto)
            self.guardar_carrito()

    def vaciar_carrito(self):
        self.session["carrito"] = {}
        self.session.modified = True
