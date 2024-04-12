from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from django.http import HttpResponse
from django.template.loader import render_to_string
from order.models import OrderItem, Order
from order.forms import OrderCreateForm ,CartAddProductForm
from order.utils.tasks import order_created
from order.utils.cart import Cart
from product.models import Product
from coupon.forms import CouponApplyForm
from rest_framework import generics ,viewsets ,views, status
# from product.recommender import Recommender
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from order.serializers import OrderItemSerializer
from django.shortcuts import get_object_or_404
from product.viewset import ProductViewSet



class OrderCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
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





class CartViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['post'])
    def cart_add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.data)

        if form.is_valid():
            cd = form.cleaned_data
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cart_remove(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart.remove(product)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def cart_update(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.data)

        if form.is_valid():
            cd = form.cleaned_data
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart.update(product=product,
                        quantity=cd['quantity'],
                        override_quantity=cd['override'])
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def cart_delete(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart.delete(product)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def list(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
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
            'cou': coupon_apply_form,
            'recommended_products': ProductSerializer(recommended_products, many=True).data})   