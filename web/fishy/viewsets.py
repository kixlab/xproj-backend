from django.shortcuts import render
from rest_framework import viewsets
from fishy.serializers import FishySerializer
from fishy.models import Fishy
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# Create your views here.

class FishyViewSet(viewsets.ModelViewSet):
    queryset = Fishy.objects.all()
    serializer_class = FishySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        queryset = fishy.objects.all()
        effect = self.request.query_params.get('effect', None)
        user = self.request.user.pk

        if effect is not None:
            queryset = queryset.filter(effect = effect)

        if user is not None:
            queryset = queryset.filter(user = user)

        return queryset

    def create(self, request):

        # fishy = self.get_object()
        data = request.data
        data['user'] = request.user.pk
        prev_fishy = Fishy.objects.filter(user=data['user']).filter(effect=data['effect'])
        serializer = FishySerializer(data = request.data)
        if serializer.is_valid() and not prev_fishy.exists():
            serializer.save()
            return Response(status=201, data='successfully voted')
        elif serializer.is_valid() and prev_fishy.exists():
            prev_fishy.delete()
            return Response(status=409, data='successfully unvoted')
        # fishy.set_effect(serializer.data['effect'])
        # fishy.set_user(request.user)

        # fishy.save()

        return Response(status= 400, data=serializer.errors)