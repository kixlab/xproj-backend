from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from promises.serializers import *
from promises.models import Person, Promise

class PromiseViewSet(viewsets.ReadOnlyModelViewSet):
    """This endpoint provides promises made by people.
    You can also access them by going through the people resource."""
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    People are members of the public holding some function, like politicians.
    You can search for them by name and access details in sub resources."""
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @detail_route()
    def promises(self, request, pk=None):
        """
        Returns a list of all the person's promises
        """
        person = self.get_object()
        promises = person.promises.all()
        context = {
            'request': request
        }
        promise_serializer = PromiseSerializer(promises, many=True, context=context)
        return Response(promise_serializer.data)