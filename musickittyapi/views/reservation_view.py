from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from musickittyapi.models import Reservation, Profile, Location
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ReservationView(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        # If the user is authenticated and is staff, show all reservations
        if request.user.is_authenticated and request.user.is_staff:
            reservations = Reservation.objects.all().order_by('date')
        elif request.user.is_authenticated:
            # If the user is authenticated but not staff, filter reservations by their profile
            reservations = Reservation.objects.filter(profile__user=request.user).order_by('date')
        else:
            # If the user is not authenticated, show an empty list or you can handle this differently
            reservations = []

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
            reservation.location = Location.objects.get(pk=request.data["location"])
            reservation.date = request.data["date"]
            reservation.time = request.data["time"]
            reservation.number_of_guests = int(request.data["number_of_guests"])  # Ensure it's an integer
            reservation.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'message': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user making the request is the owner of the reservation or a staff member
        if reservation.profile.user == request.user or request.user.is_staff:
            reservation.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You do not have permission to delete this reservation.'}, status=status.HTTP_403_FORBIDDEN)

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



