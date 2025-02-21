from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')
    progress = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Challenge(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="challenges")
    question = models.TextField()
    code_snippet = models.TextField()
    correct_answer = models.CharField(max_length=255)
    options = models.JSONField()
    challenge_type = models.CharField(max_length=20, choices=[
        ('fill_in_blank', 'Fill in the Blank'),
        ('drag_drop', 'Drag and Drop'),
        ('speed_coding', 'Speed Coding'),
        ('quiz', 'Quiz'),
        ('project', 'Project')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class UserProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
