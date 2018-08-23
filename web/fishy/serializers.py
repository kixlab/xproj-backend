from rest_framework import serializers
from fishy.models import Fishy

class FishySerializer(serializers.ModelSerializer):
    class Meta:
        model = Fishy
        fields = ('url', 'id','user', 'effect')
        