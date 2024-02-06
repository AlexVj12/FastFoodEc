class Carrito:
    def __init__(self, request):
        print(request)
        self.request = request
        self.session = request.session
        print(request.session)
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar_producto(self, producto):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "total": producto.precio,
                "imagen":producto.imagen,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["total"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar_producto(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def disminuir_producto(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["total"] -= producto.precio
            if self.carrito[id]["cantidad"] <= 0: self.eliminar_producto(producto)
            self.guardar_carrito()

    def vaciar_carrito(self):
        self.session["carrito"] = {}
        self.session.modified = True


