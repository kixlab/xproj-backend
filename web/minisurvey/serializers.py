from rest_framework import serializers
from minisurvey.models import MiniSurvey

class MiniSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniSurvey
        fields = ('url', 'id', 'created', 'user', 'policy', 'first_answer', 'second_answer', 'third_answer', 'fourth_answer', 'fifth_answer', 'article1_q1', 'article1_q2', 'article1_q3', 'article2_q1', 'article2_q2', 'article2_q3')
