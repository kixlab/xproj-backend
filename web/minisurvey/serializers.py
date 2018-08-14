from rest_framework import serializers
from minisurvey.models import MiniSurvey

class MiniSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniSurvey
        fields = ('url', 'id', 'user', 'policy', 'first_answer', 'second_answer', 'third_answer', 'fourth_answer')