from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from musickittyapi.models import Cat, Location

class CatView(ViewSet):

    def list(self, request):
        cats = Cat.objects.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single location

        Returns:
            Response -- JSON serialized location record
        """
        try:
            cat = Cat.objects.get(pk=pk)
        except Cat.DoesNotExist:
            return Response({'message': 'Cat not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized = CatSerializer(cat, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            location = Location.objects.get(pk=request.data["location"])

            cat = Cat.objects.create(
                location=location,
                name=request.data["name"],
                age=request.data["age"],
                sex=request.data["sex"],
                bio=request.data["bio"],
                image=request.data["image"],
                adopted=request.data["adopted"],
                gets_along_with_cats=request.data["gets_along_with_cats"],
                gets_along_with_dogs=request.data["gets_along_with_dogs"],
                gets_along_with_children=request.data["gets_along_with_children"]
            )
            serializer = CatSerializer(cat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            cat = Cat.objects.get(pk=pk)
        except Cat.DoesNotExist:
            return Response({'message': 'Cat not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            cat.location = Location.objects.get(pk=request.data["location"])
            cat.name = request.data["name"]
            cat.age = request.data["age"]
            cat.sex = request.data["sex"]
            cat.bio = request.data["bio"]
            cat.image = request.data["image"]
            cat.adopted = request.data["adopted"]
            cat.gets_along_with_cats = request.data["gets_along_with_cats"]
            cat.gets_along_with_dogs = request.data["gets_along_with_dogs"]
            cat.gets_along_with_children = request.data["gets_along_with_children"]
            cat.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'message': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            cat = Cat.objects.get(pk=pk)
        except Cat.DoesNotExist:
            return Response({'message': 'Cat not found.'}, status=status.HTTP_404_NOT_FOUND)
        cat.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ('id', 'location', 'name', 'age', 'sex', 'bio', 'image', 'adopted', 'gets_along_with_cats', 'gets_along_with_dogs', 'gets_along_with_children')
