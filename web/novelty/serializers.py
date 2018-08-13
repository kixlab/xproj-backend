from rest_framework import serializers
from novelty.models import Novelty

class NoveltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Novelty
        fields = ('url', 'id','user', 'effect')