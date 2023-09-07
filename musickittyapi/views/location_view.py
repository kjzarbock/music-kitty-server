from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from musickittyapi.models import Location

class LocationView(ViewSet):

    def list(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single location

        Returns:
            Response -- JSON serialized location record
        """
        try:
            location = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response({'message': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized = LocationSerializer(location, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            location = Location.objects.create(
                name=request.data["name"],
                address=request.data["address"],
                phone_number=request.data["phone_number"],
                opening_hours=request.data["opening_hours"],
                closing_hours=request.data["closing_hours"]
            )
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response({'message': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            location.name = request.data["name"]
            location.address = request.data["address"]
            location.phone_number = request.data["phone_number"]
            location.opening_hours = request.data["opening_hours"]
            location.closing_hours = request.data["closing_hours"]
            location.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response({'message': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'phone_number', 'opening_hours', 'closing_hours')
