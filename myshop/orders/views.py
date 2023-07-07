from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)  # извлекается текущая корзина из сеанса
    if request.method == 'POST':
        form = OrderCreateForm(data=request.POST)
        if form.is_valid():
            order = form.save()  # в базе данных создается новый заказ
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
