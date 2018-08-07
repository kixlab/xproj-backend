from django.shortcuts import render
from rest_framework import viewsets
from summary.serializers import SummarySerializer
from summary.models import Summary
# Create your views here.

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer