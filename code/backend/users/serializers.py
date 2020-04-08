from rest_framework import serializers

from . import models as m


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.User
        fields = "__all__"
