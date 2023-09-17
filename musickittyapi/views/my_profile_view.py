from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from musickittyapi.models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers

class MyProfileView(APIView):
    def get(self, request, format=None):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"message": "Authentication required to access this resource."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Retrieve the logged-in user's profile
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"message": "Profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def put(self, request, format=None):
          # Notice we use 'put' instead of 'update'
        try:
            profile = Profile.objects.get(user=request.user)
            profile.image = request.data.get("image", profile.image)
            profile.bio = request.data.get("bio", profile.bio)
            profile.has_cats = request.data.get("has_cats", profile.has_cats)
            profile.has_dogs = request.data.get("has_dogs", profile.has_dogs)
            profile.has_children = request.data.get("has_children", profile.has_children)
            profile.approved_to_adopt = request.data.get("approved_to_adopt", profile.approved_to_adopt)
            profile.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'is_staff')
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ('user', 'image', 'bio', 'has_cats', 'has_dogs', 'has_children', 'approved_to_adopt')
