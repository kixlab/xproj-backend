from rest_framework import serializers
from policy.models import Policy
from effect.models import Effect
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag

class VoteListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.user.pk

class EffectSerializer(TaggitSerializer, serializers.ModelSerializer):

    # flags = serializers.SerializerMethodField()
    # empathy = VoteListingField(read_only=True, many=True)
    # # serializers.SlugRelatedField(
    # #     many=True,
    # #     read_only=True,
    # #     slug_field='user'
    # # )
    # novelty = VoteListingField(read_only=True, many=True)
    # fishy = VoteListingField(read_only=True, many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Effect
        fields = ('url', 'id', 'policy', 'stakeholder_group', 'isBenefit', 'is_guess', 'stakeholder_detail', 'description', 'source', 'user', 'tags', 'confidence')

    # def get_flags(self, obj):
    #     return obj.flag.count()
        
    # def get_empathy(self, obj):
    #     return obj.empathy.

    # def get_novelty(self, obj):
    #     return obj.novelty.count()

class EffectSlugSerializer(TaggitSerializer, serializers.ModelSerializer):
    stakeholder_group = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'name'
    )
    # flags = serializers.SerializerMethodField()
    # empathy = VoteListingField(read_only=True, many=True)
    # novelty = VoteListingField(read_only=True, many=True)
    # fishy = VoteListingField(read_only=True, many=True)
    tags = TagListSerializerField()


    class Meta:
        model = Effect
        fields = ('url', 'id', 'policy', 'stakeholder_group', 'isBenefit', 'is_guess', 'stakeholder_detail', 'description', 'source', 'user', 'tags', 'confidence')
    
    # def get_flags(self, obj):
    #     return obj.flag.count()

    # def get_empathy(self, obj):
    #     return obj.empathy.count()

    # def get_novelty(self, obj):
    #     return obj.novelty.count()
    
        # read_only_fields = ('policy',)
    # def create(self, validated_data):
    #     effect = Effect()
    #     print(validated_data)
    #     return effect

# class TagSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Tag
#         fields = ()