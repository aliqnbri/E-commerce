
from django.shortcuts import render, get_object_or_404
from order.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

























# from django.shortcuts import render, get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.views.generic import ListView, DetailView
# from product.models import Product, Category, Review

# from django.core.paginator import Paginator



# class ProductListView(ListView):
#     """
#     list of products by category
#     """
#     model = Product
#     template_name = 'product/product_list.html'
#     context_object_name = 'products'
#     paginate_by = 3


#     def get_object(self, queryset=None):
#         id = self.kwargs.get('id')
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(Product, id=id, slug=slug)

#     def get_queryset(self):
#         """Queryset to include only available products ordered by created"""
#         category_slug = self.kwargs.get('category_slug')
#         queryset = Product.objects.filter(available=True).order_by('-created')
#         if category_slug:
#             category = get_object_or_404(Category, slug=category_slug)
#             products = products.objects.filter(category=category)
#         return queryset

#     # def get_context_data (self, **kwargs):

#     #     context = super().get_context_data(**kwargs)
#     #     product = self.get_object()
#     #     product_url = reverse('product_detail', args=[product.id, product.slug])
#     #     context['product_url'] = product_url
#     #     return context
#         # context = super().get_context_data(**kwargs)
#         # context['category'] = get_object_or_404(Category, slug=self.kwargs.get(
#         #     'category_slug')) if self.kwargs.get('category_slug') else None
#         # context['categories'] = Category.objects.all()
#         # return context


# class ProductDetailView(DetailView):
#     """ product deatil veiw """
#     model = Product
#     template_name = 'product/product_detail.html'
#     context_object_name = 'product'


#     def get_object(self, queryset=None):
#         id = self.kwargs.get('id')
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(Product, id=id, slug=slug, available=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         product = self.get_object()
#         context['reviews'] = product.reviews.all()
#         return context

# # class ProductListView(ListView):
# #     """
# #     List of products
# #     """
# #     model = Product
# #     template_name = 'product/index.html'
# #     context_object_name = 'products'
# #     paginate_by = 3

# #     def get_queryset(self):
# #         """queryset to include only available products"""
# #         queryset = Product.objects.filter(available=True).order_by('-created')
# #         return queryset


# # class ProductDetailView(DetailView):
# #     model = Product
# #     template_name = 'product/product_detail.html'
# #     context_object_name = 'product'

# #     def get_queryset(self):
# #         """queryset to include only available products"""
# #         queryset = Product.objects.filter(available=True).order_by('-created')
# #         return queryset

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)

# #         product = self.get_object(queryset=get_queryset())

# #         reviews = Review.objects.filter(product=product)

# #         context['reviews'] = reviews

# #         return context

# #     def get_object(self, queryset=None):
# #         """Get the product object based on the slug field"""
# #         slug = self.kwargs.get('slug')
# #         obj = Product.objects.get(slug=slug)
# #         return obj
