from tokenize import Double


def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += round(float(value["total"]),2)
    return {"total_carrito": total}