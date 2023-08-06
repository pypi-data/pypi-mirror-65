from django.db import models
from scoped_rbac.models import AccessControlledModel
from scoped_rbac.registry import ResourceType


class ScopedRbacTestModel(models.Model):
    """Mixin class for models used in testing."""

    class Meta:
        app_label = "tests"
        abstract = True


class ExampleAccessControlledModel(ScopedRbacTestModel, AccessControlledModel):
    class Meta:
        get_latest_by = "updated_at"

    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_context = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    resource_type = ResourceType(
        "rbac.ExampleAccessControlledModel",
        "ExampleAccessControlledModel",
        "An example AccessControlledModel for testing and demonstration purposes.",
    )
