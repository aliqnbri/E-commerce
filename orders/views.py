from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .models import OrderItem ,Order
from .manager import Cart
from .forms import CartAddProductForm , OrderCreateForm

# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('orders:cart_detail')

@require_POST
def cart_remove(request,porduct_id):
    cart = Cart(request)
    product = get_object_or_404(Product , id=porduct_id)
    cart.remove(product)
    return redirect ('orders:cart_detail')


def cart_detail(request):
    cart = Cart (request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return  render (request,'orders/cart_detail.html', {'cart':cart})   


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order_id=order,
                product_id=item['product'],
                price=item['price'],
                quantity=item['quantity'])
            cart.clear()
            return render (request,'orders/order/created.html',{'order':order})
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})                