# استفاده از ایمیج رسمی Python
FROM python:3.10

# تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل‌های پروژه داخل کانتینر
COPY requirements.txt requirements.txt

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه داخل کانتینر
COPY . .

# باز کردن پورت 8000
EXPOSE 8000

# اجرای سرور Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
