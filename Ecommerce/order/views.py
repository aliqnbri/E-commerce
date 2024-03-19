from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from order.models import OrderItem, Order
from order.forms import OrderCreateForm ,CartAddProductForm
from order.utils.tasks import order_created
from order.utils.cart import Cart
from django.views.decorators.http import require_POST
from product.models import Product
from coupon.forms import CouponApplyForm
from rest_framework import generics
from order.api import serializers

# from product.recommender import Recommender

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrderItemSerializer
from django.shortcuts import get_object_or_404





class CartAPIView(APIView):
    queryset = Product.objects.all()
    def get(self, request):
        cart = request.session.get('cart', {})
        return Response(cart)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session.modified = True

        return Response({'message': 'Product added to cart'})

    def put(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id] = quantity
            request.session.modified = True
            return Response({'message': 'Cart updated successfully'})
        else:
            return Response({'error': 'Product not found in cart'}, status=404)

    def delete(self, request):
        product_id = request.data.get('product_id')

        cart = request.session.get('cart', {})

        if product_id in cart:
            del cart[product_id]
            request.session.modified = True
            return Response({'message': 'Product removed from cart'})
        else:
            return Response({'error': 'Product not found in cart'}, status=404)


class OrderCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer)
        title = serializer.validated_data.get('title')
        slug = serializer.validated_data.get('slug')
        if slug is None:
            slug = title
        serializer.save()



class OrderCreateAPIView(APIView):
    queryset = OrderItem.objects.all()
    def post(self, request):
        cart = Cart(request)
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
           
            # set the order in the session
            request.session['order_id'] = order.id
            # return the created order data
            return Response(OrderCreateSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

class CartViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['post'])
    def cart_add(self, request, product_id=None):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.data)
        
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
            return redirect('cart:cart_detail')
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cart_remove(self, request, product_id=None):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


    def list(self, request):
        cart = Cart(request)
        data = []
        
        for item in cart:
            update_quantity_form = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True
            }).as_p()  # Convert form to HTML representation for JSON response

            data.append({
                'product_id': item['product'].id,
                'product_name': item['product'].name,
                'quantity': item['quantity'],
                'update_quantity_form': update_quantity_form
            })

        coupon_apply_form = CouponApplyForm().as_p()  # Convert form to HTML representation for JSON response

        r = Recommender()
        cart_products = [item['product'] for item in cart]
        if cart_products:
            recommended_products = r.suggest_products_for(cart_products, max_results=4)
        else:
            recommended_products = []

        return Response({
            'cart_items': data,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products
        })

# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  override_quantity=cd['override'])
#     return redirect('cart:cart_detail')


# # @require_POST
# # def cart_remove(request, product_id):
# #     cart = Cart(request)
# #     product = get_object_or_404(Product, id=product_id)
# #     cart.remove(product)
# #     return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if(cart_products):
        recommended_products = r.suggest_products_for(cart_products,
                                                      max_results=4)
    else:
        recommended_products = []

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,})
                #    'recommended_products': recommended_products})

def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()


# # class CartAddProductView(APIView):
# #     def post(self, request):
# #         serializer = CartAddProductSerializer(data=request.data)
# #         if serializer.is_valid():
# #             # Add product to the cart logic here
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # class ProductDetailAPIView(generics.RetrieveAPIView):
# #     """DRF API Product Detail View """
# #     serializer_class = serializers.ProductSerializer
# #     lookup_field = 'slug'
# #     # cart_product_form = CartAddProductForm()

# #     def get_queryset(self, slug=None):
# #         queryset = Product.objects.filter(
# #             slug=slug, available=True).order_by('-created')
# #         return get_object_or_404(queryset)

# #     def get(self, request, slug):
# #         product = self.get_queryset(slug=slug)
# #         serializer = self.serializer_class(product).data

# #         # r = Recommender()
# #         # recommended_products = r.suggest_products_for([product], 4)
# #         # data = {
# #         #     'product': serializer.data,
# #         #     'cart_product_form': cart_product_form,
# #         #     # 'recommended_products': recommended_products,
# #         # }
# #         return Response(serializer, status=status.HTTP_200_OK)


# class CartUpdateAPIView(generics.UpdateAPIView):
#     """DRF API cart Update View """
#     queryset = Product.objects.all()
#     serializer_class = serializers.ProductSerializer
#     lookup_field = 'slug'

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if not instance.slug:
#             instance.slug = instance.title

#         return Response(serializer, status=status.HTTP_200_OK)


# class cartDeleteAPIView(generics.DestroyAPIView):
#     """DRF API Product Update View """
#     queryset = Product.objects.all()
#     serializer_class = serializers.ProductSerializer
#     lookup_field = 'slug'

#     def perform_destroy(self, instance):
#         super().perform_destroy(instance)

#         return Response(status=status.HTTP_200_OK)














# class CartRemoveProductView(APIView):
#     def post(self, request):
#         # Remove product from the cart logic here
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CartListView(APIView):
#     def get(self, request):
#         # List products in the cart logic here
#         return Response(data, status=status.HTTP_200_OK)

# class CartDetailView(APIView):
#     def get(self, request, pk):
#         # Get details of a specific product in the cart logic here
#         return Response(data, status=status.HTTP_200_OK)







# # def order_create(request):
# #     cart = Cart(request)
# #     if request.method == 'POST':
# #         form = OrderCreateForm(request.POST)
# #         if form.is_valid():
# #             order = form.save(commit=False)
# #             if cart.coupon:
# #                 order.coupon = cart.coupon
# #                 order.discount = cart.coupon.discount
# #             order.save()
# #             for item in cart:
# #                 OrderItem.objects.create(order=order,
# #                                         product=item['product'],
# #                                         price=item['price'],
# #                                         quantity=item['quantity'])
# #             # clear the cart
# #             cart.clear()
# #             # launch asynchronous task
# #             order_created.delay(order.id)
           
# #             # set the order in the session
# #             request.session['order_id'] = order.id
# #             # redirect for payment
# #             return redirect(reverse('payment:process'))
# #     else:
# #         form = OrderCreateForm()
# #     return render(request,
# #                   'orders/order/create.html',
# #                   {'cart': cart, 'form': form})















# @staff_member_required
# def admin_order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request,
#                   'admin/orders/order/detail.html',
#                   {'order': order})


# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html',
#                             {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response,
#         stylesheets=[weasyprint.CSS(
#             settings.STATIC_ROOT / 'css/pdf.css')])
#     return response



