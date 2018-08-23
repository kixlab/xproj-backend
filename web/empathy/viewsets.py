from django.shortcuts import render
from rest_framework import viewsets
from empathy.serializers import EmpathySerializer
from empathy.models import Empathy
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# Create your views here.

class EmpathyViewSet(viewsets.ModelViewSet):
    queryset = Empathy.objects.all()
    serializer_class = EmpathySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        queryset = Empathy.objects.all()
        effect = self.request.query_params.get('effect', None)
        user = self.request.user.pk

        if effect is not None:
            queryset = queryset.filter(effect = effect)

        if user is not None:
            queryset = queryset.filter(user = user)

        return queryset

    def create(self, request):

        # empathy = self.get_object()
        data = request.data
        data['user'] = request.user.pk
        prev_empathy = Empathy.objects.filter(user=data['user']).filter(effect=data['effect'])
        serializer = EmpathySerializer(data = request.data)
        if serializer.is_valid() and not prev_empathy.exists():
            serializer.save()
            return Response(status=201, data='successfully voted')
        elif serializer.is_valid() and prev_empathy.exists():
            prev_novelty.delete()
            return Response(status=409, data='successfully unvoted')
        # empathy.set_effect(serializer.data['effect'])
        # empathy.set_user(request.user)

        # empathy.save()

        return Response(status= 400, data=serializer.errors)