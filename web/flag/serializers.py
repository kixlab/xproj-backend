from rest_framework import serializers
from flag.models import Flag

class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ('url', 'id', 'effect', 'reason')