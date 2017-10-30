from rest_framework import serializers
from promises.models import Person, Promise

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    promises_url = serializers.HyperlinkedIdentityField(view_name='person-promises')
    #province = serializers.CharField(source='mop_for_district.areas.first.province')
    #precinct = serializers.CharField(source='mop_for_district.areas.first.precinct')

    class Meta:
        model = Person
        fields = ('url', 'name', 'mop_for_district', 'promises_url', )

class PromiseSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Promise
        fields = ('url', 'title', 'categories', 'target_groups', 'person')
