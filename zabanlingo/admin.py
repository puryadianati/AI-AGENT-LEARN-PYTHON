from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # فیلدهایی که در لیست کاربران نمایش داده می‌شوند
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    
    # فیلدهایی که در صفحه ویرایش کاربر قابل ویرایش هستند
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # فیلدهایی که در صفحه ایجاد کاربر قابل ویرایش هستند
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    # فیلدهای جستجو
    search_fields = ('username', 'email', 'phone_number')
    
    # فیلدهای فیلتر
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

# ثبت مدل CustomUser با استفاده از کلاس CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)



from django.contrib import admin
from .models import CustomUser, Section, Unit, Chapter


admin.site.register(Section)
admin.site.register(Unit)
admin.site.register(Chapter)
