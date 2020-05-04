from django.http.response import HttpResponse
from django.http import JsonResponse
from rest_framework import mixins, viewsets
import os


class NoReadModelViewSet(
    # fmt: off
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Only allows adding new resources and modifying them, NO GET request allowed at all!
    It is to make sure public facing API doesn't leak information.
    A viewset that provides default `create()`, `update()`, `partial_update()`
    and `destroy()` actions.
    """


def health_check(req):
    return HttpResponse("OK")


def build_info(req):
    r = {}
    r["build"] = os.environ.get("BUILD", "n.a")
    r["commit"] = os.environ.get("COMMIT", "n.a.")
    r["branch"] = os.environ.get("BRANCH", "n.a.")
    return JsonResponse(r)
