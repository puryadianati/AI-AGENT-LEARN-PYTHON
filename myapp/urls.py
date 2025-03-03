from django.urls import path
from .views import *

urlpatterns = [
   
    path('generate-lessons/', generate_lessons, name='generate_lessons'),
    path('generate_challenges', generate_challenges),
    path('challenge/', get_random_challenge, name='get_challenge'),
     # صفحه اصلی که لیست دروس را نمایش می‌دهد
    path('', lesson_list, name='lesson_list'),
    # مسیر شروع چالش‌ها (اندیس اولیه 0)
    # Lesson challenge flow
    # urls.py
    path('lesson/<int:lesson_id>/challenge/<int:challenge_index>/', lesson_challenges, name='lesson_challenge_detail')


]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


