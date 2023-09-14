from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from musickittyapi.models import Product, Location

# Location Serializer
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'phone_number', 'opening_hours', 'closing_hours') 

# Product Serializer with expanded location information
class ProductSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'description', 'price', 'image', 'locations')

class ProductView(ViewSet):

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized = ProductSerializer(product, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            location_ids = request.data["locations"]  # assuming this is a list of location ids
            locations = Location.objects.filter(pk__in=location_ids)
            
            product = Product.objects.create(
                description=request.data["description"],
                price=request.data["price"],
                image=request.data["image"]
            )
            product.locations.set(locations)
            product.save()

            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            location_ids = request.data["locations"]
            locations = Location.objects.filter(pk__in=location_ids)
            
            product.description = request.data["description"]
            product.price = request.data["price"]
            product.image = request.data["image"]
            product.locations.set(locations)
            product.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
