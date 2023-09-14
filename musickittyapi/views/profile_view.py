from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from musickittyapi.models import Profile
from django.contrib.auth.models import User

class ProfileView(ViewSet):

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        profile = Profile.objects.get(user=request.user)
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
            # Avoiding the user assignment logic, if you want to allow updating of other fields, continue here
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
            if user.is_staff:
                return Response({"message": "User is already a staff member."}, status=status.HTTP_400_BAD_REQUEST)
            user.is_staff = True
            user.save()
            return Response({"message": "User has been granted staff status."}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ('user', 'image', 'bio', 'has_cats', 'has_dogs', 'has_children', 'approved_to_adopt')
