from rest_framework import serializers
from promises.models import Person, Promise, BudgetProgram

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    promises_url = serializers.HyperlinkedIdentityField(view_name='person-promises')
    #province = serializers.CharField(source='mop_for_district.areas.first.province')
    #precinct = serializers.CharField(source='mop_for_district.areas.first.precinct')

    class Meta:
        model = Person
        fields = ('url', 'name', 'mop_for_district', 'promises_url', 'mayor_for_province', 'mayor_for_district',)


class PromiseShortSerializer(serializers.HyperlinkedModelSerializer):
    person_name = serializers.CharField(read_only=True, source='person.name')
    
    class Meta:
        model = Promise
        fields = ('id', 'url', 'title', 'person_name')


class PromiseSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Promise
        fields = ('url', 'title', 'categories', 'target_groups', 'person')

class BudgetProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BudgetProgram
        fields = ('url', 'name', 'fiscal_year', 'category', 'sub_category', 'department', 'total_amount', )

class BudgetProgramDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BudgetProgram
        fields = (
            'url', 'name', 'fiscal_year', 'category', 'sub_category', 'department', 'total_amount',
            'original_id', 'fiscal_category', 'expenditure_amount', 'etc_amount', 'change_amount',
            'forward_amount', 'allocated_amount', 'national_amount', 'province_amount', 'precinct_amount',
            'balance_amount' 
        )