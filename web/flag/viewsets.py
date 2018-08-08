from django.shortcuts import render
from rest_framework import viewsets
from flag.serializers import FlagSerializer
from flag.models import Flag
# Create your views here.

class FlagViewSet(viewsets.ModelViewSet):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer