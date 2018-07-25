from django.shortcuts import render
from rest_framework import viewsets
from stakeholdergroup.serializers import StakeholderGroupSerializer
from stakeholdergroup.models import StakeholderGroup
# Create your views here.

class StakeholderGroupViewSet(viewsets.ModelViewSet):
    queryset = StakeholderGroup.objects.all()
    serializer_class = StakeholderGroupSerializer