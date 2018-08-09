from rest_framework import serializers
from stakeholdergroup.models import StakeholderGroup

class StakeholderGroupSerializer(serializers.ModelSerializer):
    keywords = serializers.SerializerMethodField()
    class Meta:
        model = StakeholderGroup
        fields = ('url', 'id', 'policy', 'name', 'keywords')

    def get_keywords(self, obj):
        negEffects = obj.effects.filter(isBenefit=0).order_by('empathy', 'novelty')
        posEffects = obj.effects.filter(isBenefit=1).order_by('empathy', 'novelty')
        
        negEffect = 'Negative effect not posted... yet!'
        posEffect = 'Positive effect not posted... yet!'
        
        try:
            negEffect = negEffects[0].description
        except IndexError:
            pass
        finally:
            try:
                posEffect = posEffects[0].description
            except IndexError:
                pass
            finally:
                return {'positive': posEffect, 'negative': negEffect}
