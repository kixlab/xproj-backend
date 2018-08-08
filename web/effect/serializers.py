from rest_framework import serializers
from policy.models import Policy
from effect.models import Effect
from summary.serializers import SummarySerializer
from summary.models import Summary
class EffectSerializer(serializers.ModelSerializer):
    flags = serializers.SerializerMethodField()

    class Meta:
        model = Effect
        fields = ('url', 'id', 'policy', 'stakeholder_group', 'isBenefit', 'stakeholder_detail', 'description', 'empathy', 'novelty', 'source', 'flags')

    def get_flags(self, obj):
        return obj.flag.count()

class EffectSlugSerializer(serializers.ModelSerializer):
    stakeholder_group = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'name'
    )

    class Meta:
        model = Effect
        fields = ('url', 'id', 'policy', 'stakeholder_group', 'isBenefit', 'stakeholder_detail', 'description', 'empathy', 'novelty', 'source', 'flags')
    
    def get_flags(self, obj):
        return obj.flag.count()
        # read_only_fields = ('policy',)
    # def create(self, validated_data):
    #     effect = Effect()
    #     print(validated_data)
    #     return effect