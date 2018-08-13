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
        serializer = EmpathySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200})
        # empathy.set_effect(serializer.data['effect'])
        # empathy.set_user(request.user)

        # empathy.save()

        return Response(status= 400, data=serializer.errors)