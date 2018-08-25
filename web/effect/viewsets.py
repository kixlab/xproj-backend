from django.shortcuts import render
from rest_framework import viewsets
from effect.serializers import EffectSerializer, EffectSlugSerializer
from effect.models import Effect
from stakeholdergroup.models import StakeholderGroup
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import detail_route
from rest_framework.response import Response
# Create your views here.

class EffectViewSet(viewsets.ModelViewSet):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticatedOrReadOnly, )
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
        tags = self.request.query_params.getlist('tag', None)

        if policy is not None:
            queryset = queryset.filter(policy = policy)

        if stakeholder_group is not None:
            queryset = queryset.filter(stakeholder_group = stakeholder_group)

        if tags is not None:
            queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset

    # @detail_route(methods=['post'])
    # def increment_empathy(self, request, pk=None):
    #     effect = self.get_object()
    #     user = request.user

        

    # @action(methods=['get'], detail=False)
    # def effects_by_policy(self, request):
    #     effects_by_policy = Effect.objects.filter()

    def create(self, request):
        data = request.data
        data['user'] = request.user.pk
        serializer = EffectSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Effect added successfully")

        return Response(status = 400, data = serializer.errors)
    