from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from musickittyapi.models import ProfileAdoption, Cat, Profile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

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
        fields = ['user', 'image', 'bio', 'has_cats', 'has_dogs', 'has_children', 'approved_to_adopt']

# Cat serializer
class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['id', 'name', 'location', 'age', 'sex', 'bio', 'image', 'adopted', 'gets_along_with_cats', 'gets_along_with_dogs', 'gets_along_with_children']

# ProfileAdoption serializer
class ProfileAdoptionSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    cat = CatSerializer()

    class Meta:
        model = ProfileAdoption
        fields = '__all__'

# ProfileAdoptionView
class ProfileAdoptionView(viewsets.ModelViewSet):
    queryset = ProfileAdoption.objects.select_related('profile', 'cat').all()
    serializer_class = ProfileAdoptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        profile = request.user.profile  # Get the profile associated with the authenticated user
        cat_id = request.data.get('cat_id')

        if not cat_id:
            return Response({'error': 'Cat ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        adoption_status = request.data.get('status', '')  # Get the status if provided, otherwise it's an empty string
        adoption_date = request.data.get('adoption_date')

        # Check if this profile has already adopted this cat
        if ProfileAdoption.objects.filter(profile=profile, cat_id=cat_id).exists():
            return Response({'error': 'Cat already adopted by this profile'}, status=status.HTTP_400_BAD_REQUEST)

        # If all is well, create the adoption record
        adoption_record = ProfileAdoption.objects.create(
            profile=profile,
            cat_id=cat_id,
            adoption_date=adoption_date,
            status=adoption_status
        )

        serializer = self.get_serializer(adoption_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        profile = request.user.profile
        profile_adoption_id = kwargs.get('pk')

        try:
            adoption_record = ProfileAdoption.objects.get(id=profile_adoption_id, profile=profile)
            adoption_record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProfileAdoption.DoesNotExist:
            return Response({'error': 'Adoption record not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': 'Only staff can update adoption status.'}, status=status.HTTP_403_FORBIDDEN)
        
        adoption_record = self.get_object()
        new_status = request.data.get('status')
        
        if new_status:
            adoption_record.status = new_status
            adoption_record.save()
            return Response({'message': 'Status updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)
