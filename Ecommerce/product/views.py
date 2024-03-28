from rest_framework import generics, mixins ,permissions ,authentication,viewsets,views ,status
from django.shortcuts import render, get_object_or_404
from order.forms import CartAddProductForm
from product.models import Category, Product, Review
from product import serializers
from rest_framework.response import Response


class productSearch




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    
    def get_queryset(self):
    """queryset to include only available products"""
    queryset = Product.objects.filter(available=True).order_by('-created')
    return queryset





class ProductViewSet(viewsets.ViewSet):
    def list(self,request):
        pass
    def retrive(self,request,pk=None):
        pass
    def update(self,request):
        pass
    def destroy(self,request):
        pass






# from product.recommender import Recommender
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer)
        title = serializer.validated_data.get('title')
        slug = serializer.validated_data.get('slug')
        if slug is None:
            slug = title
        serializer.save()
        # send a singnal

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('categories', None)
        
        if category:
            queryset = queryset.filter(categories=category)
        
        return queryset

class ProductMixinVeiw(mixins.CreateModelMixin,
                       mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    """DRF List and Detail APIVeiw"""
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'


    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        if slug:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        slug = serializer.validated_data.get('slug')
        if slug is None or title != slug:
            slug = title
        serializer.save()




class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all().order_by('-created')
    serializer_class = serializers.ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer)
        title = serializer.validated_data.get('title')
        slug = serializer.validated_data.get('slug')
        if slug is None:
            slug = title
        serializer.save()
        # send a singnal


class ProductDetailAPIView(generics.RetrieveAPIView):
    """DRF API Product Detail View """
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'
    # cart_product_form = CartAddProductForm()

    def get_queryset(self, slug=None):
        queryset = Product.objects.filter(
            slug=slug, available=True).order_by('-created')
        return get_object_or_404(queryset)

    def get(self, request, slug):
        product = self.get_queryset(slug=slug)
        serializer = self.serializer_class(product).data

        # r = Recommender()
        # recommended_products = r.suggest_products_for([product], 4)
        # data = {
        #     'product': serializer.data,
        #     'cart_product_form': cart_product_form,
        #     # 'recommended_products': recommended_products,
        # }
        return Response(serializer, status=status.HTTP_200_OK)


class ProductUpdateAPIView(generics.UpdateAPIView):
    """DRF API Product Update View """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.slug:
            instance.slug = instance.title

        return Response(serializer, status=status.HTTP_200_OK)


class ProductDeleteAPIView(generics.DestroyAPIView):
    """DRF API Product Update View """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

        return Response(status=status.HTTP_200_OK)


# def filter_queryset(self, queryset):
#     filter_backends = [CategoryFilter]

#     if 'geo_route' in self.request.query_params:
#         filter_backends = [GeoRouteFilter, CategoryFilter]
#     elif 'geo_point' in self.request.query_params:
#         filter_backends = [GeoPointFilter, CategoryFilter]

#     for backend in list(filter_backends):
#         queryset = backend().filter_queryset(self.request, queryset, view=self)

#     return queryset

# class ProductListView(ListView):
#     """
#     list of products by category
#     """
#     model = Product
#     # template_name = 'product/product_list.html'
#     context_object_name = 'products'
#     paginate_by = 3

#     def get_queryset(self):
#         """Queryset to include only available products ordered by created"""
#         category_slug = self.kwargs.get('category_slug')
#         queryset = Product.objects.filter(available=True).order_by('-created')
#         if category_slug:
#             category = get_object_or_404(Category, slug=category_slug)
#             products = products.objects.filter(category=category)
#         return queryset

#     def get_object(self, queryset=None):
#         id = self.kwargs.get('id')
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(Product, id=id, slug=slug)


#     def get_context_data (self, **kwargs):

#         context = super().get_context_data(**kwargs)
#         product = self.get_object()
#         product_url = reverse('product_detail', args=[product.id, product.slug])
#         context['product_url'] = product_url
#         return context
#         context = super().get_context_data(**kwargs)
#         context['category'] = get_object_or_404(Category, slug=self.kwargs.get(
#             'category_slug')) if self.kwargs.get('category_slug') else None
#         context['categories'] = Category.objects.all()
#         return context


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(categories=category)
#     return render(request,
#                   'shop/product/list.html',
#                   {'category': category,
#                    'categories': categories,
#                    'products': products})


# def product_detail(request, id, slug):
#     product = get_object_or_404(Product,
#                                 id=id,
#                                 slug=slug,
#                                 available=True)
#     cart_product_form = CartAddProductForm()
#     # r = Recommender()
#     # recommended_products = r.suggest_products_for([product], 4)
#     return render(request,
#                   'shop/product/detail.html',
#                   {'product': product,
#                    'cart_product_form': cart_product_form,})
#                 #    'recommended_products': recommended_products})




# class ProductSearch(APIView):
#     permission_classes = [AllowAny,]
#     def get(self, request):
#         products = Product.objects.all()
#         query = request.GET.get('query')

#         if not query:
#             return Response("Please provide a search query.", status=status.HTTP_400_BAD_REQUEST)

#         """Filter products based on the search query (case-insensitive search in the title field)"""
#         products = models.Product.objects.filter(title__icontains=query)

#         """Check if any products match the search query"""
#         if not products:
#             return Response("No products found for the search query.", status=status.HTTP_400_BAD_REQUEST)

#         # Serialize the products that match the search query
#         serializer = serializers.ProductSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ReviewList(APIView):
#     permission_classes = [AllowAny,]
#     def get(self, request):
#         reviews = models.Review.objects.all()
#         serializer = serializers.ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryList(APIView):
#     permission_classes = [AllowAny,]
#     def get(self, request):
#         categories = models.Category.objects.all()
#         serializer = serializers.CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render, get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.views.generic import ListView, DetailView
# from product.models import Product, Category, Review

# from django.core.paginator import Paginator


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



