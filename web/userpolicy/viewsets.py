from django.shortcuts import render
from rest_framework import viewsets
from userpolicy.serializers import UserPolicySerializer
from userpolicy.models import UserPolicy
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class UserPolicyViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = UserPolicy.objects.all()
    serializer_class = UserPolicySerializer
    # return userPolicy ID

    def get_queryset(self):
        queryset = UserPolicy.objects.all()
        policy = self.request.query_params.get('policy', None)
        user = self.request.query_params.get('user', None)

        if policy is not None:
            queryset = queryset.filter(policy = policy)

        if user is not None:
            queryset = queryset.filter(user = user)

        return queryset