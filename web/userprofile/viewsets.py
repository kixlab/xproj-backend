from django.shortcuts import render
from rest_framework import viewsets
from userprofile.serializers import UserProfileSerializer
from userprofile.models import UserProfile
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # return UserProfile ID

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        user = self.request.user

        if user is not None:
            queryset = queryset.filter(user = user.pk)

        return queryset