from rest_framework import serializers
from spatial.models import Area, VotingDistrict
from promises.serializers import PersonSerializer

class VotingDistrictSerializer(serializers.HyperlinkedModelSerializer):
    #current_mop = serializers.HyperlinkedRelatedField(many=False, view_name='person-detail', read_only=True)
    current_mop = PersonSerializer()

    class Meta:
        model = VotingDistrict
        fields = ('url', 'name', 'current_mop')

class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        fields = ('url', 'name', 'precinct', 'province', 'voting_district_name', 'voting_district', )

class AreaDistanceSerializer(serializers.HyperlinkedModelSerializer):
    distance = serializers.CharField()

    class Meta:
        model = Area
        fields = ('url', 'name', 'precinct', 'province', 'voting_district_name', 'voting_district', 'distance', )
