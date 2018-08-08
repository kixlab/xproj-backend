from django.shortcuts import render
from rest_framework import viewsets
from effect.serializers import EffectSerializer, EffectSlugSerializer
from effect.models import Effect
from rest_framework.permissions import AllowAny
# from rest_framework.decorators import action
# Create your views here.

class EffectViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer

    def get_serializer_class(self):
        serializer_class = EffectSerializer
        get_stakeholder_names = self.request.query_params.get('get_stakeholder_names', None)

        if get_stakeholder_names is not None:
            serializer_class = EffectSlugSerializer
        
        return serializer_class


    def get_queryset(self):
        queryset = Effect.objects.all()
        policy = self.request.query_params.get('policy', None)
        stakeholder_group = self.request.query_params.get('stakeholder_group', None)

        if policy is not None:
            queryset = queryset.filter(policy = policy)

        if stakeholder_group is not None:
            queryset = queryset.filter(stakeholder_group = stakeholder_group)

        return queryset

    # @action(methods=['get'], detail=False)
    # def effects_by_policy(self, request):
    #     effects_by_policy = Effect.objects.filter()
    # def create(self, request):
    #     effect = self.get_object()

    #     serializer = EffectSerializer(data = request.data)

    #     effect.set_policy(serializer.data['policy'])
    #     effect.set_isBenefit(serializer.data['isBenefit'])
    #     effect.set_stakeholder_group(serializer.data['stakeholder_group'])
    #     effect.set_description(serializer.data['description'])
    #     effect.set_stakeholder_detail(serializer.data['stakeholder_detail'])
    #     effect.set_empathy(serializer.data['empathy'])
    #     effect.set_novelty(serializer.data['novelty'])
    #     effect.set_source(serializer.data['source'])

    #     effect.save()

    #     return Response({'status': 'effect set'})
    