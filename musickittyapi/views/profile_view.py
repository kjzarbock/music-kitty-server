from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from musickittyapi.models import Profile
from django.contrib.auth.models import User

class ProfileView(ViewSet):

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        profile = Profile.objects.get(user=request.user)
        if request.method == 'PUT':
            # Update the profile fields
            profile.image = request.data.get("image", profile.image)
            profile.bio = request.data.get("bio", profile.bio)
            profile.has_cats = request.data.get("has_cats", profile.has_cats)
            profile.has_dogs = request.data.get("has_dogs", profile.has_dogs)
            profile.has_children = request.data.get("has_children", profile.has_children)
            profile.approved_to_adopt = request.data.get("approved_to_adopt", profile.approved_to_adopt)
            profile.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    def list(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
            serialized = ProfileSerializer(profile, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
            # Update the profile fields
            profile.image = request.data.get("image", profile.image)
            profile.bio = request.data.get("bio", profile.bio)
            profile.has_cats = request.data.get("has_cats", profile.has_cats)
            profile.has_dogs = request.data.get("has_dogs", profile.has_dogs)
            profile.has_children = request.data.get("has_children", profile.has_children)
            profile.approved_to_adopt = request.data.get("approved_to_adopt", profile.approved_to_adopt)
            profile.save()
            # Serialize and return the updated profile data
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
            profile.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def set_staff_status(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
            user = profile.user
            user.is_staff = not user.is_staff  # Toggle the 'is_staff' field
            user.save()
            return Response({"message": "User staff status has been updated."}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'is_staff')
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)

    class Meta:
        model = Profile
        fields = ('user', 'image', 'bio', 'has_cats', 'has_dogs', 'has_children', 'approved_to_adopt')
