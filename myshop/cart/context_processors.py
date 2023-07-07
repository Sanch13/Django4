from .cart import Cart


def cart(request):
    """создается экземпляр класса Сart с объектом request в качестве параметра и обеспечивается
    его доступность для шаблонов в виде переменной cart"""
    return {"cart": Cart(request=request)}
