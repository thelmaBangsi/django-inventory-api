from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from inventory.services.product_service import ProductService
from inventory.apis.serializers import ProductSerializer

class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = ProductService.list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            product = ProductService.create_product(request.data)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = ProductService.get_product_by_id(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            product = ProductService.update_product(pk, request.data)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ProductService.delete_product(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
