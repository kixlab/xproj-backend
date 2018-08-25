from django.shortcuts import render
from rest_framework import viewsets
from effect.serializers import EffectSerializer, EffectSlugSerializer
from effect.models import Effect
from stakeholdergroup.models import StakeholderGroup
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer
from django.db.models import Count, Q, F

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

        if len(tags) > 0:
            queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset

    @list_route(methods=['get'])
    def tag_list(self, request):
        policy = self.request.query_params.get('policy', None)
        tags = Tag.objects.all()

        Qobj = Q(content_object__policy__exact = policy) if policy is not None else None
        Qpos = Q(content_object__isBenefit__exact = 1)
        Qpos = Qpos & Qobj if Qobj is not None else Qpos
        Qneg = Q(content_object__isBenefit__exact = 0)
        Qneg = Qneg & Qobj if Qobj is not None else Qneg
        
        # if Qobj is not None:
        #     tags = tags.annotate(
        #         refs = Count("effect_taggedeffect_items", filter=Qobj), 
        #         # positives = Count("effect_taggedeffect_items", distinct=True, filter=Q(content_object__isBenefit__exact=1)),
        #         # negatives = Count("effect_taggedeffect_items", distinct=True, filter=Q(content_object__isBenefit__exact=0)),
        #     )
        #     tags = tags.filter(refs__gt = 0)
        # query = tags.query
        # print('tag_list %s' % query)
        tag_list = [
            {
                "name": tag.name,
                "refs": tag.effect_taggedeffect_items.filter(Qobj).count() if Qobj is not None else tag.effect_tagged_effect_items.count(),
                "positive": tag.effect_taggedeffect_items.filter(Qpos).count(),
                "negative": tag.effect_taggedeffect_items.filter(Qneg).count(),
            } for tag in tags
        ]

        return Response(data=tag_list, status=200)

    @list_route(methods=['get'])
    def tag_info(self, request):
        tag = self.request.query_params.get('tag', None)
        queryset = Effect.objects.all().filter(tags__name__in=[tag]).distinct()
        
        posCount = queryset.filter(isBenefit = 1).count()
        negCount = queryset.filter(isBenefit = 0).count()

        return Response(status=200, data={
            "tag": tag,
            "refs": posCount + negCount,
            "positive": posCount,
            "negative": negCount
        })
        

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
    