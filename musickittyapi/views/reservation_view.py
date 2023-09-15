from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from musickittyapi.models import Reservation, Profile, Location
from django.contrib.auth.models import User

class ReservationView(ViewSet):

    def list(self, request):
        # Filter reservations by the authenticated user's profile and order by date
        reservations = Reservation.objects.filter(profile__user=request.user).order_by('date')

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product record
        """
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'message': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized = ReservationSerializer(reservation, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            location = Location.objects.get(pk=request.data["location"])
            profile = Profile.objects.get(pk=request.data["profile"])

            reservation = Reservation.objects.create(
                profile = profile,
                location = location,
                date = request.data["date"],
                time = request.data["time"],
                number_of_guests = request.data["number_of_guests"]
            )
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'message': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            reservation.profile = Profile.objects.get(pk=request.data["profile"])
            reservation.location = Location.objects.get(pk=request.data["location"])
            reservation.date = request.data["date"]
            reservation.time = request.data["time"]
            reservation.number_of_guests = request.data["number_of_guests"]
            reservation.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'message': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
        reservation.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ReservationProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = Profile
        fields = ('user', 'has_cats', 'has_dogs', 'has_children', 'approved_to_adopt')


class ReservationLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'phone_number', 'opening_hours', 'closing_hours')

    
class ReservationSerializer(serializers.ModelSerializer):
    profile = ReservationProfileSerializer(many=False)
    location = ReservationLocationSerializer(many=False)
    class Meta:
        model = Reservation
        fields = ('id', 'profile', 'location', 'date', 'time', 'number_of_guests')

