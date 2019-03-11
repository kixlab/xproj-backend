from django.shortcuts import render
from rest_framework import viewsets
from minisurvey.serializers import MiniSurveySerializer
from minisurvey.models import MiniSurvey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.http import HttpResponse
import csv
# Create your views here.

class MiniSurveyViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = MiniSurvey.objects.all()
    serializer_class = MiniSurveySerializer
    # return minisurvey ID

    def get_queryset(self):
        queryset = MiniSurvey.objects.all()
        policy = self.request.query_params.get('policy', None)
        user = self.request.user.pk

        if policy is not None:
            queryset = queryset.filter(policy = policy)

        if user is not None:
            queryset = queryset.filter(user = user)

        return queryset

    def create(self, request):
        data = request.data
        data['user'] = request.user.pk
        serializer = MiniSurveySerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Result added successfully")

        return Response(status = 400, data = serializer.errors)
    
    @list_route(methods=['get'])	
    def get_csv(self, request):
        response = HttpResponse(content_type='text_csv')
        response['Content-Disposition'] = 'attachment; filename="minisurveys.csv"'


        writer = csv.writer(response)
        for m in MiniSurvey.objects.all():
            writer.writerow([m.user, m.policy, m.created])
        return response
