from django.shortcuts import render
from rest_framework import viewsets
from effect.serializers import EffectSerializer
from effect.models import Effect
from rest_framework.permissions import AllowAny
# Create your views here.

class EffectViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer


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
    