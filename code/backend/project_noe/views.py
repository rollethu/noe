from rest_framework import mixins, viewsets


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
