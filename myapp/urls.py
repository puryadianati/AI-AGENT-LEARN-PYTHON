from django.urls import path
from .views import *

urlpatterns = [
   
    path('generate-lessons/', generate_lessons, name='generate_lessons'),
    path('generate_challenges', generate_challenges),
    path('challenge/', get_random_challenge, name='get_challenge'),
    path('', lesson_list, name='lesson_list'),



]
