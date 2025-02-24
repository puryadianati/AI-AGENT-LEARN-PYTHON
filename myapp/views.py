import re
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Lesson, Challenge
from openai import OpenAI
from django.shortcuts import render, get_object_or_404



client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def extract_json(raw_text: str) -> str:
    """
    در صورت وجود ``` یا ```json در متن،
    محتوای داخل آن را جدا می‌کند و برمی‌گرداند.
    اگر پیدا نشد، کل متن را برمی‌گرداند.
    """
    pattern = r"```(?:json)?(.*?)```"
    matches = re.findall(pattern, raw_text, flags=re.DOTALL)

    if matches:
        # اگر چند بلاک وجود داشت، فعلاً اولی را برمی‌داریم
        return matches[0].strip()
    else:
        return raw_text.strip()

@api_view(['POST'])
def generate_lessons(request):
    """
    Generates lessons for each syllabus topic.
    """
    syllabus = request.data.get("syllabus")

    if not syllabus:
        return Response({"error": "Syllabus data is required"}, status=400)

    # پرامپت را طوری تنظیم می‌کنیم که خروجی مستقیماً JSON باشد
    prompt = f"""
    Generate detailed lessons for the following Python topics (in valid JSON format ONLY):
    {syllabus}
    Requirements:
    1. Return ONLY valid JSON (no triple backticks or markdown).
    2. Each lesson should be an object with "title", "description", and "level" (beginner/intermediate/advanced).
    Return a list of these lesson objects, for example:
    [
      {{
        "title": "...",
        "description": "...",
        "level": "beginner"
      }},
      ...
    ]
    """

    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ]
            }
        ]
    )

    lesson_data = completion.choices[0].message.content

    if not lesson_data:
        return Response({"error": "AI response was empty or invalid"}, status=500)

    # حذف بک‌تیک‌های سه‌تایی (در صورت وجود)
    raw_json = extract_json(lesson_data)

    try:
        lessons = json.loads(raw_json)
        for lesson in lessons:
            Lesson.objects.create(
                title=lesson["title"],
                description=lesson["description"],
                level=lesson["level"]
            )
        return Response({"message": "Lessons generated and saved!"})
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON received from AI", "raw_response": lesson_data}, status=500)


import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lesson, Challenge
from .utils import extract_json  # تابع استخراج JSON از قبل تعریف شده

@api_view(['POST'])
def generate_challenges(request):
    """
    Generate AI-powered challenges for all lessons.
    """
    lessons = Lesson.objects.all()
    total_created = 0
    total_errors = []

    for lesson in lessons:
        # ساخت پرامپت سفارشی برای هر درس به گونه‌ای که تعداد چالش‌ها به صورت جامع و کافی تولید شود.
        prompt = f"""
        Generate a comprehensive set of diverse programming challenges for this Python lesson (return valid JSON ONLY):
        
        **Lesson Title**: {lesson.title}
        **Description**: {lesson.description}
        **Difficulty Level**: {lesson.level.capitalize()}
        
        Requirements:
        1. Return ONLY a JSON array of challenge objects.
        2. Each challenge must include:
           - question: Clear problem statement.
           - code_snippet: Python code related to the question (optional).
           - correct_answer: Exact expected answer.
           - options: Array of 4-5 choices (even for non-quiz types).
           - challenge_type: One of [{', '.join([ct[0] for ct in Challenge._meta.get_field('challenge_type').choices])}].
        3. Vary challenge types naturally.
        4. Match difficulty to lesson level.
        5. Generate as many challenges as necessary to comprehensively cover the lesson content.
        
        Example response:
        [
          {{
            "question": "Complete the function to calculate factorial:",
            "code_snippet": "def factorial(n):\\n    # Your code here",
            "correct_answer": "return 1 if n == 0 else n * factorial(n-1)",
            "options": [
              "return n * factorial(n-1)",
              "return 1 if n == 0 else n * factorial(n-1)",
              "if n == 0: return 1\\nreturn n * factorial(n-1)",
              "return math.factorial(n)"
            ],
            "challenge_type": "fill_in_blank"
          }},
          {{
            "question": "Arrange the code to implement bubble sort:",
            "code_snippet": "def bubble_sort(arr):\\n    n = len(arr)",
            "correct_answer": ["for i in range(n):", "for j in range(0, n-i-1):", "if arr[j] > arr[j+1]:", "arr[j], arr[j+1] = arr[j+1], arr[j]"],
            "options": [
              ["if arr[j] > arr[j+1]:", "arr[j], arr[j+1] = arr[j+1], arr[j]", "for i in range(n):", "for j in range(0, n-i-1):"],
              ["for i in range(n):", "for j in range(0, n-i-1):", "if arr[j] > arr[j+1]:", "arr[j], arr[j+1] = arr[j+1], arr[j]"]
            ],
            "challenge_type": "drag_drop"
          }}
        ]
        """

        try:
            # ارسال پرامپت به API هوش مصنوعی
            completion = client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=[{"role": "user", "content": prompt}]
            )
            raw_response = completion.choices[0].message.content
            challenges_data = json.loads(extract_json(raw_response))
        except Exception as e:
            total_errors.append({
                "lesson_id": lesson.id,
                "error": str(e)
            })
            continue

        created = 0
        for idx, challenge in enumerate(challenges_data):
            try:
                Challenge.objects.create(
                    lesson=lesson,
                    question=challenge['question'],
                    code_snippet=challenge.get('code_snippet', ''),
                    correct_answer=str(challenge['correct_answer']),
                    options=challenge['options'],
                    challenge_type=challenge['challenge_type']
                )
                created += 1
            except Exception as e:
                total_errors.append({
                    "lesson_id": lesson.id,
                    "challenge_index": idx,
                    "error": str(e),
                    "data": challenge
                })
        total_created += created

    return Response({
        "message": f"Successfully created {total_created} challenges across all lessons.",
        "errors": total_errors if total_errors else None
    })



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Challenge
from .serializers import ChallengeSerializer

def get_random_challenge(request):
    challenge = Lesson.objects.first()  # Get a random challenge
    if not challenge:
        return JsonResponse({'error': 'No challenges found'}, status=404)

    serializer = ChallengeSerializer(challenge)
    return JsonResponse(serializer.data, safe=False)


from django.shortcuts import render, get_object_or_404
from .models import Lesson

def lesson_list(request):
    lesson_data = {
        'beginner': Lesson.objects.filter(level='beginner'),
        'intermediate': Lesson.objects.filter(level='intermediate'),
        'advanced': Lesson.objects.filter(level='advanced'),
    }
    return render(request, 'courses/index.html', {'lesson_data': lesson_data})
from django.shortcuts import render, get_object_or_404
from django.http import Http404
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Lesson, Challenge

def lesson_challenges(request, lesson_id, challenge_index=0):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Create challenge sequence (5 of each type)
    challenges = []
    challenge_types = ['fill_in_blank', 'drag_drop', 'speed_coding', 'quiz', 'project']
    
    # Validate template existence
    valid_templates = {
        'fill_in_blank': 'fill_in_blank.html',
        'drag_drop': 'drag_drop.html',
        'speed_coding': 'speed_coding.html',
        'quiz': 'quiz.html',
        'project': 'project.html'  # Add this template if needed
    }
    
    # Build challenge sequence
    for challenge_type in challenge_types:
        try:
            challenges.extend(
                lesson.challenges.filter(challenge_type=challenge_type)[:5]
            )
        except KeyError:
            raise Http404(f"Invalid challenge type: {challenge_type}")

    # Handle completion state
    if challenge_index >= len(challenges):
        return render(request, 'challenges/lesson_complete.html', {
            'lesson': lesson
        })
    
    current_challenge = challenges[challenge_index]
    
    # Prepare challenge data for JSON serialization
    challenge_data = {
        'id': current_challenge.id,
        'question': current_challenge.question,
        'code_snippet': current_challenge.code_snippet,
        'correct_answer': current_challenge.correct_answer,
        'options': current_challenge.options,
        'challenge_type': current_challenge.challenge_type,
        'next_url': f"/api/lessons/{lesson_id}/challenges/{challenge_index + 1}/"
    }
    
    # Generate next URL
    next_url = f"api/lesson/{lesson_id}/challenges/{challenge_index + 1}/"
    
    # Verify template exists
    template_name = valid_templates.get(current_challenge.challenge_type)
    if not template_name:
        raise Http404(f"No template for challenge type: {current_challenge.challenge_type}")
    
    return render(request, f'challenges/{template_name}', {
        'lesson': lesson,
        'challenge_json': json.dumps(challenge_data, cls=DjangoJSONEncoder),
        'next_url': next_url,
        'challenge_type': current_challenge.challenge_type
    })