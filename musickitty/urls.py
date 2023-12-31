from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from musickittyapi.views import register_user, login_user
from rest_framework import routers
from musickittyapi.views import LocationView, CatView, ProductView, ProfileView, ReservationView, CatFavoriteView, ProfileAdoptionView, MyProfileView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'locations', LocationView, 'location')
router.register(r'cats', CatView, 'cat')
router.register(r'products', ProductView, 'product')
router.register(r'profiles', ProfileView, 'profile')
router.register(r'reservations', ReservationView, 'reservation')
router.register(r'cat-favorites', CatFavoriteView, 'catfavorite')
router.register(r'profile-adoptions', ProfileAdoptionView, 'profileadoption')

# Extending the URL patterns of the router.
profile_list = ProfileView.as_view({
    'put': 'set_staff_status'
})

profile_me = ProfileView.as_view({
    'get': 'me',
    'put': 'me'
})


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('profiles/me/', profile_me, name='profile_me'),
    path('profiles/<int:pk>/set_staff_status/', profile_list, name='set_staff_status'),
    path('locations/<int:location_id>/cats/', LocationView.as_view({'get': 'cats_by_location'})),
    path('cats/<int:pk>/', CatView.as_view({'put': 'update'}), name='cat-update'),
    path('', include(router.urls))
]
