from rest_framework import routers
from rest_framework.views import get_view_name as original_get_view_name

class KoreaDataAPI(routers.APIRootView):
    """
    REST API exposing public data about Korean administration in an easily consumable way.

    Part of the research efforts at [KIXLAB](http://kixlab.org).

    This is a self-describing API. You can browse all public endpoints at the actual API URLs.

    Most of the 'read' actions are currently public, whereas writing data requires authentication.
    """
    pass

class Router(routers.DefaultRouter):
    include_format_suffixes = False
    APIRootView = KoreaDataAPI

def get_view_name(cls, suffix=None):
    name = original_get_view_name(cls, suffix)
    # Cosmetic hack for proper view_name of detail resource
    if cls.__name__ == 'PersonViewSet' and suffix is None:
        return 'Promises'
    return name