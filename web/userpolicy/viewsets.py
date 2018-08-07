from django.shortcuts import render
from rest_framework import viewsets
from userpolicy.serializers import UserPolicySerializer
from userpolicy.models import UserPolicy
# Create your views here.

class UserPolicyViewSet(viewsets.ModelViewSet):
    queryset = UserPolicy.objects.all()
    serializer_class = UserPolicySerializer