<<<<<<< HEAD
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from inventory.models import Product
from inventory.serializers.product_serializers import ProductSerializer
from inventory.services.product_service import ProductService
from rest_framework.permissions import AllowAny 
from django.contrib.auth.models import User 
from inventory.serializers.user_serializers import RegisterSerializer  
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.db.models import Q

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

class ProductListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        products = Product.objects.all().order_by('id')
        category = request.query_params.get('category')
        if category:
            products = products.filter(category__iexact=category)
        name = request.query_params.get('name')
        if name:
            products = products.filter(name__icontains=name)
        price = request.query_params.get('price')
        if price: 
            products = products.filter(price=price)
        stock = request.query_params.get('stock')
        if stock: 
            products = products.filter(stock=stock)   

        min_stock = request.query_params.get('min_stock')
        if min_stock: 
            products = products.filter(stock__gte=min_stock)

        # Only paginate if 'page' query param is explicitly requested
        if 'page' in request.query_params:
            paginator = PageNumberPagination()
            paginated_products = paginator.paginate_queryset(products, request, view=self)
            if paginated_products is not None:
                serializer = ProductSerializer(paginated_products, many=True)
                return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request): 
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = ProductService.register_product(serializer.validated_data)
                response_serializer = ProductSerializer(product)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e: 
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try: 
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                setattr(product, attr, value)
            product.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk): 
        product = self.get_object(pk)
        if not product: 
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        # Returns HTTP 200 to match test_delete_product_returns_200 expectation
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request): 
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "username": user.username, 
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            try: 
                user = User.objects.get(pk=pk)
                serializer = RegisterSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist: 
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        users = User.objects.all()
        username = request.query_params.get('username')
        if username:
            users = users.filter(username__icontains=username)
        email = request.query_params.get('email')
        if email:
            users = users.filter(email__icontains=email)
        search = request.query_params.get('search')
        if search:
            users = users.filter(
                Q(username__icontains=search) | Q(email__icontains=search)
            )

        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
=======
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product
from .serializers import ProductSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Enable filtering by category, search by name/category, and sorting
    filterset_fields = ['category']
    search_fields = ['name', 'category']
    ordering_fields = ['price', 'stock', 'id', 'name']
    ordering = ['id']


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
