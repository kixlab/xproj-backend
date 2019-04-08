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
from effect.taghelpers import TagTree, TagTreeEncoder, TagCoOccur
import json
from .nlp import get_top_n_words_from_tfidf_kor, get_keywords
from django.http import HttpResponse
# Create your views here.

class EffectPagination(PageNumberPagination):
    page_size = 250 
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
    tag_cooccur = [None, None]
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
        exclude_tags = self.request.query_params.getlist('exclude_tag[]', None)
        # order_by = self.request.query_params.get('order_by', None)
        if policy is not None:
            queryset = queryset.filter(policy = policy)

        if stakeholder_group is not None:
            queryset = queryset.filter(stakeholder_group = stakeholder_group)
        
        queryset = queryset.exclude(source="exp_guess")
        
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

        if len(exclude_tags) > 0:
            queryset = queryset.exclude(tags__name__in=exclude_tags)

        # queryset = queryset.annotate(
        #     empathy_count = Count("empathy", distinct=True),
        #     novelty_count = Count("novelty", distinct=True),
        #     fishy_count = Count("fishy", distinct=True),
        #     score = F('empathy_count') + F('novelty_count'),
        # )
        # if tags is None or len(tags) <= 0:
        #     self.keywords = []
        # if queryset.count() >= 10 and isBenefit is not None:
        #     corpus = list(queryset.values_list('description', flat=True))
        #     query = queryset.query
        #     self.keywords = get_top_n_words_from_tfidf_kor(corpus, query, 10)
        # el
        if queryset.count() >= 10:
            self.keywords = get_keywords(queryset, 'all')

        if isBenefit is not None:
            queryset = queryset.filter(isBenefit = isBenefit)
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
            if self.tag_cooccur[ppp] is None:
                Qobj = Q(content_object__policy__exact = policy) & Q(content_object__is_guess = False)
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
                    name = tag.name
                    pos_count = query.filter(Qpos).count()
                    neg_count = query.filter(Qneg).count()
                    total_count = pos_count + neg_count
                    if total_count > 0:
                        tag_list.append((name, total_count, pos_count, neg_count))

                self.tag_cooccur[ppp] = TagCoOccur(tag_list, policy)

            self.tag_tree[ppp] = TagTree(self.tag_cooccur[ppp])

       
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
    def tag_info2(self, request):
        tag = self.request.query_params.get('tag', None)
        policy = self.request.query_params.get('policy', None)

        if policy is None:
            return Response(status = 400, data = "Please specify policy idx")

        ppp = int(policy) - 1

        if self.tag_cooccur[ppp] is None:
            tags = Tag.objects.filter(effect__policy__exact = policy).distinct()
            Qobj = Q(content_object__policy__exact = policy) & Q(content_object__is_guess = False)
            Qpos = Q(content_object__isBenefit = 1)
            Qneg = Q(content_object__isBenefit = 0)

            tag_list = []

            for t in tags:
                query = t.effect_taggedeffect_items.filter(Qobj)
                name = t.name
                pos_count = query.filter(Qpos).count()
                neg_count = query.filter(Qneg).count()
                total_count = pos_count + neg_count
                if total_count > 0:
                    tag_list.append((name, total_count, pos_count, neg_count))

            self.tag_cooccur[ppp] = TagCoOccur(tag_list, policy)
        # queryset = Effect.objects.filter(is_guess = False).filter(tags__name__in=[tag]).distinct()
        # keywords = get_keywords(queryset, 'all')
        closest = self.tag_cooccur[ppp].closest(tag)
        farthest = self.tag_cooccur[ppp].farthest(tag)
        different = self.tag_cooccur[ppp].most_different(tag)
        most_pos = self.tag_cooccur[ppp].most_positive(tag)
        most_neg = self.tag_cooccur[ppp].most_negative(tag)
        counts = self.tag_cooccur[ppp].get_counts(tag)
        return Response(status=200, data={
            "tag": tag,
            "refs": counts[1],
            "positive": counts[2],
            "negative": counts[3],
            "closest": closest,
            "farthest": farthest,
            "different": different,
            "most_pos": most_pos,
            "most_neg": most_neg,
        })

    @list_route(methods=['get'])
    def tag_info3(self, request):
        tag_high = self.request.query_params.get('tag_high', None)
        tag_low = self.request.query_params.get('tag_low', None)
        policy = self.request.query_params.get('policy', None)

        if policy is None:
            return Response(status = 400, data = "Please specify policy idx")

        ppp = int(policy) - 1

        if self.tag_cooccur[ppp] is None:
            tags = Tag.objects.filter(effect__policy__exact = policy).distinct()
            Qobj = Q(content_object__policy__exact = policy) & Q(content_object__is_guess = False)
            Qpos = Q(content_object__isBenefit = 1)
            Qneg = Q(content_object__isBenefit = 0)

            tag_list = []

            for t in tags:
                query = t.effect_taggedeffect_items.filter(Qobj)
                name = t.name
                pos_count = query.filter(Qpos).count()
                neg_count = query.filter(Qneg).count()
                total_count = pos_count + neg_count
                if total_count > 0:
                    tag_list.append((name, total_count, pos_count, neg_count))

            self.tag_cooccur[ppp] = TagCoOccur(tag_list, policy)

        # closest = self.tag_cooccur[ppp].fetch_closest(tag)
        # farthest = self.tag_cooccur[ppp].fetch_farthest(tag)
        # different = self.tag_cooccur[ppp].fetch_different(tag)
        # queryset = Effect.objects.filter(is_guess = False).filter(tags__name__in=[tag]).filter(tags__name__in=[tag]).distinct()
        farthest_group = self.tag_cooccur[ppp].farthest_group(tag_high, tag_low)
        farthest_subgroup = self.tag_cooccur[ppp].farthest_subgroup(tag_high, tag_low)
        cooccur_counts = self.tag_cooccur[ppp].get_cooccur_counts(tag_high, tag_low)
        return Response(status=200, data={
            "tag_high": tag_high,
            "tag_low": tag_low,
            "farthest_group": farthest_group,
            "farthest_subgroup": farthest_subgroup,
            "total_count": cooccur_counts[0],
            "pos_count": cooccur_counts[1],
            "neg_count": cooccur_counts[2]
            # "refs": posCount + negCount,
            # "positive": posCount,
            # "negative": negCount,
            # "closest": closest,
            # "farthest": farthest,
            # "different": different
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

        #return Response(data=myJson, status=200)
    @list_route(methods=['get'])
    def random(self, request):
        policy = self.request.query_params.get('policy', None)
        exclude = self.request.query_params.getlist('exclude[]')
        tag = self.request.query_params.get('tag', None)
        is_pos = self.request.query_params.get('is_pos', None)
        both = self.request.query_params.get('both', False)

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
        if both:
            queryset_pos = queryset.filter(isBenefit = 1)
            count_pos = queryset_pos.count()
            queryset_neg = queryset.filter(isBenefit = 0)
            count_neg = queryset_neg.count()
            obj_pos = None
            obj_neg = None

            if count_pos > 0:
                idx = random.randint(0, count_pos-1)
                obj_pos = queryset_pos[idx]
            if count_neg > 0:
                idx = random.randint(0, count_neg-1)
                obj_neg = queryset_neg[idx]
            serializer = EffectSerializer([obj_pos, obj_neg], many = True, context={'request': self.request})
            return Response(status = 200, data=serializer.data)
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
    
