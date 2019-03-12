from django.shortcuts import render
from rest_framework import viewsets
from effect.serializers import EffectSerializer, EffectSlugSerializer
from effect.models import Effect
from stakeholdergroup.models import StakeholderGroup
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer
from django.db.models import Count, Q, F, Sum
from django.db.models.functions import Length
import random
from effect.taghelpers import TagTree, TagTreeEncoder
import json
from .nlp import get_top_n_words_from_tfidf_kor
from django.http import HttpResponse
# Create your views here.

class EffectPagination(PageNumberPagination):
    page_size = 50 
    page_size_query_param = 'page_size'
    # max_page_size = 500

    def get_paginated_response(self, data, keywords):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'prev': self.get_previous_link(),
            'keywords': keywords,
            'results': data
        })
    
class EffectViewSet(viewsets.ModelViewSet):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer
    pagination_class = EffectPagination
    tag_tree = [None, None]
    keywords = []
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
        tags = self.request.query_params.getlist('tag[]', None)
        isBenefit = self.request.query_params.get('is_benefit', None)
        is_and = self.request.query_params.get('is_and', False)
        include_guess = self.request.query_params.get('include_guess', None)
        # order_by = self.request.query_params.get('order_by', None)
        if policy is not None:
            queryset = queryset.filter(policy = policy)

        if stakeholder_group is not None:
            queryset = queryset.filter(stakeholder_group = stakeholder_group)

        if isBenefit is not None:
            queryset = queryset.filter(isBenefit = isBenefit)
        
        if include_guess is not None:
            if include_guess == '1':
                queryset = queryset.filter(is_guess=True)
            elif include_guess == '0':
                queryset = queryset.filter(is_guess=False)
        
        if len(tags) > 0 and not is_and:
            queryset = queryset.filter(tags__name__in=tags).distinct()

        elif len(tags) > 0 and is_and:
            for tag in tags:
                queryset = queryset.filter(tags__name__in=[tag])

        # queryset = queryset.annotate(
        #     empathy_count = Count("empathy", distinct=True),
        #     novelty_count = Count("novelty", distinct=True),
        #     fishy_count = Count("fishy", distinct=True),
        #     score = F('empathy_count') + F('novelty_count'),
        # )
        if queryset.count() >= 10:
            corpus = list(queryset.values_list('description', flat=True))
            query = queryset.query
            self.keywords = get_top_n_words_from_tfidf_kor(corpus, query, 10)
        # if order_by == 'random':
        #     pass
        # elif order_by == 'votes':
        #     queryset = queryset.order_by('-score')
        # elif order_by == 'age':
        #     queryset = queryset.order_by('created')
        # elif order_by == 'agd_desc':
        #     queryset = queryset.order_by('-created')
        # elif order_by == 'length':
        #     queryset = queryset.order_by('-description_length')
        return queryset

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data, self.keywords)

    @list_route(methods=['get'])
    def tag_list(self, request):
        policy = self.request.query_params.get('policy', None)
        tags = Tag.objects.all()

        if policy is None:
            return Response(status = 400, data = "Please specify policy idx")

        Qobj = Q(content_object__policy__exact = policy)
        Qpos = Q(content_object__isBenefit = 1)
        # Qpos = Qpos & Qobj
        Qneg = Q(content_object__isBenefit = 0)
        # Qneg = Qneg & Qobj
        tags = tags.filter(effect__policy__exact = policy).distinct()
        # tags = tags.annotate(
        #     refs = Count("effect"), 
        #     positives = Count("effect", filter=Qpos),
        #     negatives = Count("effect", filter=Qneg),
        # )
        # tags = tags.annotate(
        #     negatives = Count("effect_taggedeffect_items", distinct=True, filter=Qneg),
        # )
        # tags = tags.filter(refs__gt = 0)
        # query = tags.query
        # print('tag_list %s' % query)
        tag_list = []

        for tag in tags:
            query = tag.effect_taggedeffect_items.filter(Qobj)
            total_count = query.count()
            name = tag.name
            pos_count = query.filter(Qpos).count()
            neg_count = query.filter(Qneg).count()
            tag_list.append({
                "name": name,
                "total_count": total_count,
                "positive": pos_count,
                "negative": neg_count,
            })
        
        #TODO: find more optimal way
        # tag_list = [
        #     {
        #         "name": tag.name,
        #         "refs": tag.effect_taggedeffect_items.filter(Qobj).count(),
        #         "positive": tag.effect_taggedeffect_items.filter(Qpos).count(),
        #         "negative": tag.effect_taggedeffect_items.filter(Qneg).count(),
        #     } for tag in tags
        # ]

        return Response(data=tag_list, status=200)

    @list_route(methods=['get'])
    def tag_list2(self, request):
        policy = self.request.query_params.get('policy', None)
        tags = Tag.objects.all()

        if policy is None:
            return Response(status = 400, data = "Please specify policy idx")

        ppp = int(policy) - 1

        if self.tag_tree[ppp] is None or self.tag_tree[ppp].isEmpty():
            self.tag_tree[ppp] = TagTree()
            Qobj = Q(content_object__policy__exact = policy)
            Qpos = Q(content_object__isBenefit = 1)
            # Qpos = Qpos & Qobj
            Qneg = Q(content_object__isBenefit = 0)
            # Qneg = Qneg & Qobj
            tags = tags.filter(effect__policy__exact = policy).distinct()
            # tags = tags.annotate(
            #     refs = Count("effect"), 
            #     positives = Count("effect", filter=Qpos),
            #     negatives = Count("effect", filter=Qneg),
            # )
            # tags = tags.annotate(
            #     negatives = Count("effect_taggedeffect_items", distinct=True, filter=Qneg),
            # )
            # tags = tags.filter(refs__gt = 0)
            # query = tags.query
            # print('tag_list %s' % query)
            tag_list = []

            for tag in tags:
                query = tag.effect_taggedeffect_items.filter(Qobj)
                total_count = query.count()
                name = tag.name
                pos_count = query.filter(Qpos).count()
                neg_count = query.filter(Qneg).count()
                tag_list.append((name, total_count, pos_count, neg_count))

            self.tag_tree[ppp].construct_tag_tree(tag_list)

       
        myJson = json.dumps(self.tag_tree[ppp].root, cls=TagTreeEncoder, ensure_ascii = False)
        
        #TODO: find more optimal way
        # tag_list = [
        #     {
        #         "name": tag.name,
        #         "refs": tag.effect_taggedeffect_items.filter(Qobj).count(),
        #         "positive": tag.effect_taggedeffect_items.filter(Qpos).count(),
        #         "negative": tag.effect_taggedeffect_items.filter(Qneg).count(),
        #     } for tag in tags
        # ]

        #return Response(data=myJson, status=200)
        return HttpResponse(myJson, content_type="application/json")

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

    @list_route(methods=['get'])
    def random(self, request):
        policy = self.request.query_params.get('policy', None)
        exclude = self.request.query_params.getlist('exclude[]')
        tag = self.request.query_params.get('tag', None)
        is_pos = self.request.query_params.get('is_pos', None)

        if policy is None:
            return Response(status = 400, data = "Please specify policy idx")

        queryset = Effect.objects.filter(policy = policy)
        if is_pos is not None:
            queryset = queryset.filter(isBenefit = is_pos)
        if tag is not None:
            queryset = queryset.filter(tags__name__in=[tag])
        if len(exclude) > 0:
            queryset = queryset.exclude(id__in=exclude)

        # queryset = queryset.annotate(
        #     empathy_count = Count("empathy", distinct=True),
        #     novelty_count = Count("novelty", distinct=True),
        #     fishy_count = Count("fishy", distinct=True),
        #     score = F('empathy_count') + F('novelty_count')
        # )
        # # queryset = queryset.annotate(
        # #     score = Sum(F('empathy_count'), F('novelty_count'))
        # # )

        # queryset = queryset.filter(score__gte=1)
        count = queryset.count()

        if (count == 0):
            return Response(status=404, data = "no such effect")
        while True:
            idx = random.randint(0, count-1)
            obj = queryset[idx]

            serializer = EffectSerializer(obj, context={'request': self.request})
            return Response(status = 200, data=serializer.data)

    # @list_route(methods=['get'])
    # def get_keywords(self, request):
    #     queryset = Effect.objects.all()
    #     policy = self.request.query_params.get('policy', None)
    #     tags = self.request.query_params.getlist('tag[]', None)
    #     isBenefit = self.request.query_params.get('is_benefit', None)
    #     is_and = self.request.query_params.get('is_and', False)
    #     include_guess = self.request.query_params.get('include_guess', None)

    #     if policy is not None:
    #         queryset = queryset.filter(policy = policy)

    #     if isBenefit is not None:
    #         queryset = queryset.filter(isBenefit = isBenefit)
        
    #     if include_guess is not None:
    #         if include_guess == '1':
    #             queryset = queryset.filter(is_guess=True)
    #         elif include_guess == '0':
    #             queryset = queryset.filter(is_guess=False)
        
    #     if len(tags) > 0 and not is_and:
    #         queryset = queryset.filter(tags__name__in=tags).distinct()

    #     elif len(tags) > 0 and is_and:
    #         for tag in tags:
    #             queryset = queryset.filter(tags__name__in=[tag])

    #     queryset = queryset.annotate(
    #         empathy_count = Count("empathy", distinct=True),
    #         novelty_count = Count("novelty", distinct=True),
    #         fishy_count = Count("fishy", distinct=True),
    #         score = F('empathy_count') + F('novelty_count')
    #     )
    #     corpus = list(queryset.values_list('description', flat=True))
    #     keywords = get_top_n_words_from_tfidf_kor(corpus, n=10)
    #     queryset = queryset.order_by('-score')

    #     serializer = EffectSerializer(queryset, context={'request': self.request})
    #     res = Response(serializer.data)
    #     res.data['keywords'] = keywords
    #     return res

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
    
