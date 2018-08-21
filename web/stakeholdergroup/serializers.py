from rest_framework import serializers
from stakeholdergroup.models import StakeholderGroup

class StakeholderGroupSerializer(serializers.ModelSerializer):
    keywords = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()
    class Meta:
        model = StakeholderGroup
        fields = ('url', 'id', 'policy', 'name', 'keywords', 'is_visible', 'counts')

    def get_keywords(self, obj):
        negEffects = obj.effects.filter(isBenefit=0).order_by('empathy', 'novelty')
        posEffects = obj.effects.filter(isBenefit=1).order_by('empathy', 'novelty')
        
        negEffect = '아직 부정적 효과가 없어요. 클릭하신 뒤 직접 추가해주세요!'
        posEffect = '아직 긍정적 효과가 없어요. 클릭하신 뒤 직접 추가해주세요!'
        
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

    def get_counts(self, obj):
        negEffects = obj.effects.filter(isBenefit=0).count()
        posEffects = obj.effects.filter(isBenefit=1).count()

        return {'positive': posEffects, 'negative': negEffects}
