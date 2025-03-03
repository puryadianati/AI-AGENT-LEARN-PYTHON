from django.contrib import admin
from .models import UserProfile, Lesson, Challenge, UserProgress

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'level', 'progress', 'score', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('level',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'created_at')
    search_fields = ('title',)
    list_filter = ('level',)

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question', 'challenge_type', 'created_at')
    search_fields = ('question', 'lesson__title')
    list_filter = ('challenge_type',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score', 'updated_at')
    search_fields = ('user__username', 'lesson__title')
    list_filter = ('completed',)
