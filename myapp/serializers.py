from rest_framework import serializers
from .models import *

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
