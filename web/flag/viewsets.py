from django.shortcuts import render
from rest_framework import viewsets
from flag.serializers import FlagSerializer
from flag.models import Flag
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class FlagViewSet(viewsets.ModelViewSet):
    permission_class = (IsAuthenticatedOrReadOnly, )
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer