from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from musickittyapi.models import Profile

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token, _ = Token.objects.get_or_create(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'staff': authenticated_user.is_staff
        }
        return Response(data)
    else:
        data = {'valid': False}
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    password = request.data.get('password', None)
    bio = request.data.get('bio', '')
    image = request.data.get('image', '')
    has_cats = request.data.get('has_cats', False)
    has_dogs = request.data.get('has_dogs', False)
    has_children = request.data.get('has_children', False)

    if email is not None \
            and first_name is not None \
            and last_name is not None \
            and password is not None:

        try:
            new_user = User.objects.create_user(
                username=request.data['username'],
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            Profile.objects.create(
                user=new_user,
                bio=bio,
                image=image,
                has_cats=has_cats,
                has_dogs=has_dogs,
                has_children=has_children
            )

        except IntegrityError:
            return Response(
                {'message': 'An account with that email address or username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=new_user)
        data = {'token': token.key}
        return Response(data)

    return Response({'message': 'You must provide email, password, first_name, and last_name'}, status=status.HTTP_400_BAD_REQUEST)
