from django.shortcuts import render
from rest_framework import viewsets
from policy.serializers import PolicySerializer
from policy.models import Policy
# Create your views here.

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer