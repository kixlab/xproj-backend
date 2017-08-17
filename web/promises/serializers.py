from rest_framework import serializers
from promises.models import Person, Promise

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    promises_url = serializers.HyperlinkedIdentityField(view_name='person-promises')

    class Meta:
        model = Person
        fields = ('url', 'name', 'mop_for_district', 'promises_url')

class PromiseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promise
        fields = ('url', 'title', 'categories', 'target_groups',)
