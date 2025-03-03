from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  CustomUserCreationForm  # اگر از فرم‌های جنگو استفاده می‌کنید



def index(request):
    return render(request, 'index.html')


def language_page(request, lang):
    context = {
        'selected_lang': lang
    }
    return render(request, 'language.html', context)

from .forms import EmailAuthenticationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        
        messages.error(request, 'Invalid email or password')
    else:
        form = EmailAuthenticationForm()

    return render(request, 'loginpage.html', {'form': form})

# در views.py
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    context = {
        'user': request.user
    }
    return render(request, 'zaban/dashboard.html', context)