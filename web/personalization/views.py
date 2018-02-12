from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from prompt_responses.models import PromptSet
from rest_framework.exceptions import NotAuthenticated
from .utils import get_promptset_prompt

class PersonalizedPromptset(APIView):
    "Return a personalized prompt string for a prompt set"
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = PromptSet.objects

    def get(self, request, name, format=None):
        user = request.user
        #if not user or not user.is_authenticated:
        #    raise NotAuthenticated()

        prompt_set = get_object_or_404(PromptSet, name=name)
        object_id = request.query_params.get('object_id', None)
        
        text = get_promptset_prompt(prompt_set, object_id, user)

        data = {
            'user': str(user),
            'text': text
        }
        return Response(data)