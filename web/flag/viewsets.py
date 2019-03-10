from django.shortcuts import render
from rest_framework import viewsets
from flag.serializers import FlagSerializer
from flag.models import Flag
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Create your views here.

class FlagViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer

    def get_queryset(self):
        queryset = Flag.objects.all()
        effect = self.request.query_params.get('effect', None)
        user = self.request.user.pk

        if effect is not None:
            queryset = queryset.filter(effect = effect)

        if user is not None:
            queryset = queryset.filter(user = user)

        return queryset

    def create(self, request):

        # Flag = self.get_object()
        data = request.data
        data['user'] = request.user.pk
        serializer = FlagSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = 200)
        # Flag.set_effect(serializer.data['effect'])
        # Flag.set_user(request.user)

        # Flag.save()

        return Response(status= 400, data=serializer.errors)