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

        if policy is not None:
            queryset = queryset.filter(policy = policy)

        return queryset

    # @action(methods=['get'], detail=False)
    # def effects_by_policy(self, request):
    #     effects_by_policy = Effect.objects.filter()
    # def create(self, request):
    #     effect = self.get_object()

    #     serializer = EffectSerializer(data = request.data)

    #     effect.set_policy(serializer.data['policy'])
    #     effect.set_isBenefit(serializer.data['isBenefit'])
    #     effect.set_identity(serializer.data['identity'])
    #     effect.set_description(serializer.data['description'])
    #     effect.set_oneliner(serializer.data['oneliner'])
    #     effect.set_likes(serializer.data['likes'])

    #     effect.save()

    #     return Response({'statue': 'effect set'})
    