from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('language/<str:lang>/', language_page, name='language'),
    path('login/',login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    
    # Password reset views

    path('dashboard/',dashboard, name='dashboard'),



    ]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


