# views.py
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from musickittyapi.models import CatFavorite, Cat, Profile, Location 
from django.contrib.auth.models import User

class CatFavoriteView(viewsets.ModelViewSet):
    # We will initialize the serializer_class later after defining the serializers
    queryset = CatFavorite.objects.select_related('profile', 'cat', 'cat__location').all()

    def create(self, request, *args, **kwargs):
        profile = request.user.profile  # assuming the request user has a profile associated
        cat_id = request.data.get('cat_id')

        if not cat_id:
            return Response({'error': 'Cat ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        cat_favorite, created = CatFavorite.objects.get_or_create(profile=profile, cat_id=cat_id)

        if not created:
            return Response({'error': 'Already favorited'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CatFavoriteSerializer(cat_favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        profile = request.user.profile  # assuming the request user has a profile associated
        cat_id = kwargs.get('pk')  # assuming you pass the cat_id as the primary key to delete

        try:
            cat_favorite = CatFavorite.objects.get(profile=profile, cat_id=cat_id)
            cat_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CatFavorite.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user',]

# Location serializer
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'address']

# Cat serializer
class CatSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Cat
        fields = ['id', 'name', 'image', 'location']

class CatFavoriteSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    cat = CatSerializer()
    class Meta:
        model = CatFavorite
        fields = '__all__'

# Now, we set the serializer_class attribute of CatFavoriteView after defining the serializer
CatFavoriteView.serializer_class = CatFavoriteSerializer
