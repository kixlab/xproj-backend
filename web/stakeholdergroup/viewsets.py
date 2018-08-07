from django.shortcuts import render
from rest_framework import viewsets
from stakeholdergroup.serializers import StakeholderGroupSerializer
from stakeholdergroup.models import StakeholderGroup
# Create your views here.

class StakeholderGroupViewSet(viewsets.ModelViewSet):
    serializer_class = StakeholderGroupSerializer
    queryset = StakeholderGroup.objects.all()
    def get_queryset(self):
        queryset = StakeholderGroup.objects.all()
        policy = self.request.query_params.get('policy', None)

        if policy is not None:
            queryset = queryset.filter(policy = policy)

        return queryset