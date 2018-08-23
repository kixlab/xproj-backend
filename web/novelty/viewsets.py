from django.shortcuts import render
from rest_framework import viewsets
from novelty.serializers import NoveltySerializer
from novelty.models import Novelty
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# Create your views here.

class NoveltyViewSet(viewsets.ModelViewSet):
    queryset = Novelty.objects.all()
    serializer_class = NoveltySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        queryset = Novelty.objects.all()
        effect = self.request.query_params.get('effect', None)
        user = self.request.user.pk

        if effect is not None:
            queryset = queryset.filter(effect = effect)

        if user is not None:
            queryset = queryset.filter(user = user)

        return queryset

    def create(self, request):

        # Novelty = self.get_object()
        data = request.data
        data['user'] = request.user.pk
        serializer = NoveltySerializer(data = request.data)
        prev_novelty = Novelty.objects.filter(user=data['user']).filter(effect=data['effect'])

        if serializer.is_valid() and not (prev_novelty.exists()):
            serializer.save()
            return Response(status=201, data='successfully voted')
        elif serializer.is_valid() and prev_novelty.exists():
            prev_novelty.delete()
            return Response(status=409, data='successfully unvoted')
        # Novelty.set_effect(serializer.data['effect'])
        # Novelty.set_user(request.user)

        # Novelty.save()

        return Response(status= 400, data=serializer.errors)