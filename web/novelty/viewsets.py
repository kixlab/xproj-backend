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
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200})
        # Novelty.set_effect(serializer.data['effect'])
        # Novelty.set_user(request.user)

        # Novelty.save()

        return Response(status= 400, data=serializer.errors)