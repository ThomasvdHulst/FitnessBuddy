from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('exercises', views.exercises, name='exercises'),
    path('search_exercises', views.search_exercises, name='search_exercises'),
    path('profile', views.profile, name='profile'),
    path('startworkout', views.startworkout, name='startworkout'),
    path('workout', views.workout, name='workout'),

]