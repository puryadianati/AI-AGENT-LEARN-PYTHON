# myproject/myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class CustomUser(AbstractUser):
    # Fields from the original CustomUser
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)  # Keep as IntegerField
    name = models.CharField(max_length=100, blank=True)
    hearts = models.IntegerField(default=3)
    current_lesson = models.IntegerField(default=1)
    completed_units = models.IntegerField(default=0)
    completed_chapters = models.IntegerField(default=0)
    gems = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    learn_lang = models.CharField(max_length=10, default='de')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    section_number = models.IntegerField(default=1)  # Added from UserProfile
    creation_date = models.DateTimeField(auto_now_add=True) # Added from UserProfile
    email = models.EmailField(unique=True)  # Mark email as unique
    USERNAME_FIELD = 'email'  # استفاده از ایمیل برای ورود
    REQUIRED_FIELDS = ['username']  # فیلدهای ضروری دیگر


    # Handling related_name conflicts (IMPORTANT)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",  # Use a unique related_name
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  # Use the *same* related_name as groups
        related_query_name="customuser",
    )

    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Section(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)  # Store image filename, not the full path
    # totalChaptersInUnit and totalUnitsInSection are not needed as model fields
    # They can be calculated dynamically.

    def __str__(self):
        return self.name

    @property
    def total_units(self):
        return self.units.count()


class Unit(models.Model):
    section = models.ForeignKey(Section, related_name='units', on_delete=models.CASCADE)
    unit_number = models.PositiveIntegerField()  # Explicit unit number
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.section.name} - {self.name}"

    class Meta:
        ordering = ['section', 'unit_number']  # Order by section, then unit number

    @property
    def total_chapters(self):
        return self.chapters.count()

class Chapter(models.Model):
    unit = models.ForeignKey(Unit, related_name='chapters', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.unit.name} - {self.name}"

    class Meta:
        ordering = ['unit', 'id']  # Consistent ordering

