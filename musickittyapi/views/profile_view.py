from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from musickittyapi.models import Profile
from django.contrib.auth.models import User

class ProfileView(ViewSet):

    def list(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single profile

        Returns:
            Response -- JSON serialized profile record
        """
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized = ProfileSerializer(profile, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = User.objects.get(pk=request.data["user"])
            profile.user = user
            profile.image = request.data["image"]
            profile.bio = request.data["bio"]
            profile.has_cats = request.data["has_cats"]
            profile.has_dogs = request.data["has_dogs"]
            profile.has_children = request.data["has_children"]
            profile.approved_to_adopt = request.data["approved_to_adopt"]

            profile.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        profile.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'username')
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ('user', 'image', 'bio', 'has_cats', 'has_dogs', 'has_children', 'approved_to_adopt')

