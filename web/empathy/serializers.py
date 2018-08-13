from rest_framework import serializers
from empathy.models import Empathy

class EmpathySerializer(serializers.ModelSerializer):
    class Meta:
        model = Empathy
        fields = ('url', 'id','user', 'effect')
        