from rest_framework import viewsets

from . import models as m
from . import serializers as s


class UserViewSet(viewsets.ModelViewSet):
    queryset = m.User.objects.all()
    serializer_class = s.UserSerializer
