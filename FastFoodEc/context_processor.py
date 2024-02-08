from tokenize import Double


def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        carrito_session = request.session.get("carrito")
        if carrito_session:
            for _, value in carrito_session.items():
                total += round(float(value["total"]), 2)
    return {"total_carrito": total}