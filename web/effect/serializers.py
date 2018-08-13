from rest_framework import serializers
from policy.models import Policy
from effect.models import Effect
from summary.serializers import SummarySerializer
from summary.models import Summary
class EffectSerializer(serializers.ModelSerializer):
    flags = serializers.SerializerMethodField()
    empathy = serializers.SerializerMethodField()
    novelty = serializers.SerializerMethodField()

    class Meta:
        model = Effect
        fields = ('url', 'id', 'policy', 'stakeholder_group', 'isBenefit', 'stakeholder_detail', 'description', 'empathy', 'novelty', 'source', 'flags', 'user')

    def get_flags(self, obj):
        return obj.flag.count()
        
    def get_empathy(self, obj):
        return obj.empathy.count()

    def get_novelty(self, obj):
        return obj.novelty.count()

class EffectSlugSerializer(serializers.ModelSerializer):
    stakeholder_group = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'name'
    )
    flags = serializers.SerializerMethodField()
    empathy = serializers.SerializerMethodField()
    novelty = serializers.SerializerMethodField()

    class Meta:
        model = Effect
        fields = ('url', 'id', 'policy', 'stakeholder_group', 'isBenefit', 'stakeholder_detail', 'description', 'empathy', 'novelty', 'source', 'flags', 'user')
    
    def get_flags(self, obj):
        return obj.flag.count()

    def get_empathy(self, obj):
        return obj.empathy.count()

    def get_novelty(self, obj):
        return obj.novelty.count()
    
        # read_only_fields = ('policy',)
    # def create(self, validated_data):
    #     effect = Effect()
    #     print(validated_data)
    #     return effect