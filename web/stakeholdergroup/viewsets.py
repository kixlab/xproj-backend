from django.shortcuts import render
from rest_framework import viewsets
from stakeholdergroup.serializers import StakeholderGroupSerializer
from stakeholdergroup.models import StakeholderGroup
from rest_framework.response import Response

# Create your views here.

class StakeholderGroupViewSet(viewsets.ModelViewSet):
    serializer_class = StakeholderGroupSerializer
    queryset = StakeholderGroup.objects.all()

    def get_queryset(self):
        queryset = StakeholderGroup.objects.filter(is_visible = True)
        policy = self.request.query_params.get('policy', None)

        if policy is not None:
            queryset = queryset.filter(policy = policy)

        return queryset

    def create(self, request):
        data = request.data
        data['author'] = request.user.pk
        serializer = StakeholderGroupSerializer(data = request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)

        return Response(status = 400, data = serializer.errors)