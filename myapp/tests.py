from myapp.models import *

# درس ۱: مقدمه پایتون (سطح Beginner)
lesson1 = Lesson.objects.create(
    title="مقدمه پایتون",
    description="در این درس با مفاهیم اولیه پایتون آشنا می‌شویم و مبانی برنامه‌نویسی را یاد می‌گیریم.",
    level="beginner"
)

LessonDetail.objects.create(
    lesson=lesson1,
    overview="این درس یک مرور کلی از مبانی پایتون است.",
    objectives="آشنایی با syntax پایتون، متغیرها، و توابع اولیه",
    content="محتوای تکمیلی شامل مثال‌های کدنویسی و تمرین‌های عملی",
    resources='["https://docs.python.org/3/tutorial/"]'
)

# چالش‌های مربوط به درس ۱
challenge1 = Challenge.objects.create(
    lesson=lesson1,
    order=1,
    question="کدام یک از موارد زیر برای تعریف یک تابع در پایتون استفاده می‌شود؟",
    code_snippet="def my_function():\n    return 'Hello World'",
    correct_answer="def",
    options='["function", "def", "lambda", "class"]',
    challenge_type="quiz"
)

challenge2 = Challenge.objects.create(
    lesson=lesson1,
    order=2,
    question="خروجی کد زیر چیست؟",
    code_snippet="print(2 + 3 * 4)",
    correct_answer="14",
    options='["20", "14", "18", "12"]',
    challenge_type="quiz"
)

# درس ۲: توابع در پایتون (سطح Intermediate)
lesson2 = Lesson.objects.create(
    title="توابع در پایتون",
    description="در این درس به مباحث مربوط به توابع و نحوه استفاده از آن‌ها در برنامه‌نویسی می‌پردازیم.",
    level="intermediate"
)

LessonDetail.objects.create(
    lesson=lesson2,
    overview="این درس به معرفی توابع، پارامترها و بازگشت مقادیر می‌پردازد.",
    objectives="نوشتن توابع ساده، استفاده از توابع تو در تو و درک مفهوم بازگشت مقادیر",
    content="مثال‌های عملی از نحوه تعریف و استفاده از توابع در پروژه‌های واقعی",
    resources='["https://realpython.com/defining-your-own-python-function/"]'
)

# چالش مربوط به درس ۲
challenge3 = Challenge.objects.create(
    lesson=lesson2,
    order=1,
    question="خروجی کد زیر چیست؟",
    code_snippet="""
def add(a, b):
    return a + b

print(add(5, 7))
""",
    correct_answer="12",
    options='["10", "12", "15", "None"]',
    challenge_type="speed_coding"
)

# درس ۳: مفاهیم پیشرفته پایتون (سطح Advanced)
lesson3 = Lesson.objects.create(
    title="مفاهیم پیشرفته پایتون",
    description="در این درس به مباحث پیشرفته مانند generator ها، decorators و context managers می‌پردازیم.",
    level="advanced"
)

LessonDetail.objects.create(
    lesson=lesson3,
    overview="این درس برای توسعه‌دهندگان حرفه‌ای طراحی شده و به بررسی عمیق مفاهیم پایتون می‌پردازد.",
    objectives="درک عمیق generator ها، decorators و نحوه مدیریت منابع در برنامه",
    content="تمرین‌های پیشرفته و مثال‌های کاربردی از استفاده در پروژه‌های بزرگ",
    resources='["https://realpython.com/primer-on-python-decorators/"]'
)

challenge4 = Challenge.objects.create(
    lesson=lesson3,
    order=1,
    question="کدام یک از موارد زیر مربوط به کاربرد generator در پایتون است؟",
    code_snippet="def my_generator():\n    yield 1\n    yield 2",
    correct_answer="yield",
    options='["return", "yield", "break", "continue"]',
    challenge_type="fill_in_blank"
)
