from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),  # مسیر برای ورود
    path('register/', RegisterView.as_view(), name='register'),  # URL برای ثبت‌نام



    ]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


