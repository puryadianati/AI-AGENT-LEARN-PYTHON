from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User



from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django_ratelimit.decorators import ratelimit



   
@method_decorator(csrf_protect, name='dispatch')
class LoginView(View): 
    def get(self, request):
        return render(request, 'loginpage.html')
    def post(self, request):
        # Parse JSON data from the request body
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            validate_email(email)
            if not password:
                return JsonResponse({"success": False, "message": "Invalid email or password."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid email or password."}, status=400)
        except ValidationError:
            return JsonResponse({"success": False, "message": "Invalid email or password."}, status=400)

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"success": False, "message": "Invalid email or password."}, status=401)
def index(request):
    return render(request,'index.html')


import json
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from zabanlingo.models import CustomUser
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
     def get(self, request):
        return render(request, 'signup.html')
     def post(self, request):
        try:
            # دریافت داده‌ها از درخواست
            data = json.loads(request.body)
            # دریافت مقادیر از داده‌های ورودی
            age = data.get('age')
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            # اعتبارسنجی مقادیر
            if not age:
                return JsonResponse({"success": False, "message": "Age is required."}, status=400)
            if not name:
                return JsonResponse({"success": False, "message": "Name is required."}, status=400)
            if not email:
                return JsonResponse({"success": False, "message": "Email is required."}, status=400)
            if not password:
                return JsonResponse({"success": False, "message": "Password is required."}, status=400)
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({"success": False, "message": "invalid-email"}, status=400)

            if len(password) < 6:
                return JsonResponse({"success": False, "message": "weak-password"}, status=400)

            # ایجاد کاربر جدید
            try:
                user = CustomUser.objects.create(
                    email=email,
                    username=email,  # استفاده از ایمیل به عنوان نام کاربری
                    password=make_password(password),  # رمز عبور هش شده
                    age=age,
                    name=name,
                    gems=500,  # مقدار پیش‌فرض
                    hearts=3,  # مقدار پیش‌فرض
                    xp=0,  # مقدار پیش‌فرض
                    section_number=1,  # مقدار پیش‌فرض
                    completed_units=0,  # مقدار پیش‌فرض
                    completed_chapters=0,  # مقدار پیش‌فرض
                    current_lesson=1,  # مقدار پیش‌فرض
                )
                user.save()

                return JsonResponse({
                    "success": True,
                    "message": "Account created successfully.",
                    "userId": user.id
                }, status=201)

            except IntegrityError:
                return JsonResponse({"success": False, "message": "email-already-in-use"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)