from rest_framework import permissions
from .models import RoleAssignment
from . import policy
from .rbac_contexts import DEFAULT_CONTEXT, SOME_CONTEXT


NOT_ALLOWED = policy.RootPolicy().add_policy(policy.POLICY_FALSE)
ALLOWED = policy.RootPolicy().add_policy(policy.POLICY_TRUE)


def policy_for(request):
    # TODO figure out caching for this
    if request.user is None or request.user.is_anonymous:
        return NOT_ALLOWED
    if request.user.is_superuser:
        return ALLOWED
    role_assignments = RoleAssignment.objects.filter(
        user=request.user
    ).prefetch_related("role")
    total_policy = policy.RootPolicy()
    policy_by_role = dict()
    for role_assignment in role_assignments.all():
        role = role_assignment.role
        if role not in policy_by_role:
            policy_by_role[role] = role.as_policy
        policy_for_role = policy_by_role[role]
        total_policy.add_policy_for_context(
            policy_for_role, role_assignment.rbac_context
        )
        total_policy.add_policy_for_context(policy_for_role, SOME_CONTEXT)
    return total_policy


def http_action_iri_for(request):
    return f"http.{request.method}"


class IsAuthorized(permissions.BasePermission):
    """
    Custom permission handling using the `rbac` model.
    """

    def has_object_permission(self, request, view, obj):
        """
        Requires that the object is `AccessControlled`.
        """
        if not hasattr(view, "resource_type_iri_for"):
            return True
        effective_policy = policy_for(request)
        ret = effective_policy.should_allow(
            policy.Permission(http_action_iri_for(request), obj.resource_type.iri),
            obj.rbac_context,
            obj,
        )
        return ret

    def has_permission(self, request, view):
        """
        Requires the view to be an `AccessControlledAPIView`.
        """
        if not hasattr(view, "resource_type_iri_for"):
            return True
        effective_policy = policy_for(request)
        if request.method in ("PUT", "POST"):
            resource = request.data if request.method in ("PUT", "POST") else None
            rbac_context = resource.get("rbac_context", DEFAULT_CONTEXT)
        else:
            resource = None
            rbac_context = SOME_CONTEXT
        ret = effective_policy.should_allow(
            policy.Permission(
                http_action_iri_for(request), view.resource_type_iri_for(request)
            ),
            rbac_context,
            resource,
        )
        return ret
