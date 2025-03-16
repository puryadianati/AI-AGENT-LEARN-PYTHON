from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'hearts', 
            'current_lesson',
            'completed_units',
            'completed_chapters',
            'gems',
            'xp',
            'learn_lang',
            # Add other needed fields
        ]