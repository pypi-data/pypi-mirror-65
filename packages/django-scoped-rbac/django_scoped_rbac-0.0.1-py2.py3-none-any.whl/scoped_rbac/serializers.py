from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Role, RoleAssignment


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RoleAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User Serialization"""

    class Meta:
        model = User
        fields = ("url", "username", "email", "first_name", "last_name", "id")
