from rest_framework import serializers
from stakeholdergroup.models import StakeholderGroup


class StakeholderGroupSerializer(serializers.ModelSerializer):
    keywords = serializers.SerializerMethodField()
    class Meta:
        model = StakeholderGroup
        fields = ('url', 'id', 'policy', 'name', 'keywords')

    def get_keywords(self, obj):
        effects = obj.effects.all()
        # TODO: Implement TF-IDF? Keyword extraction
        return [effect.description for effect in effects]
