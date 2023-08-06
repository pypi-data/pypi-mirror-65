************
Introduction
************


Django Scoped RBAC provides a sophisticated implementation of role-based and attribute
based access control. Django Scoped RBAC differs from most role-based access control
libraries in that roles are assigned within specific security scopes called *"contexts"*
rather than within the application as a whole.

Concepts
========

Permission
----------

A *permission* is a tuple ``(action, resource-type)``. For example, ``(GET,
http://example.com/rdf/2019/Address)``

Permission Policy
-----------------

A *permission-policy* is a tuple ``(action, resource-type, policy)``. For example,
``(GET, http://example.com/rdf/2019/Address, True)``


Action
------

An action is any verb that makes sense for the application domain. For example, a Django
REST API should use the HTTP verbs ``(GET, PUT, POST, DELETE, etc.)`` as actions.

Resource-Type
-------------

A URI indicating a resource type. For a Django REST API, this would indicate the type of
the resource protected. As an example, a User resource might have an RDF type URI like
``http://django.com/rdf/2019/User``.

Policy
------

A policy indicates whether the action is allowed (``True``), or not allowed (``False``),
or is dependent upon the successful evaluation of a policy expression.

Role
----

A *Role* is a collection of permissions.

Context
-------

A *Context* is a scope within which permissions can be evaluated for a given
resource-type. For example, a project with resources whose access is restricted to
members of the project depending upon the role or roles they play in the project.

Role-Assignment
---------------

An association of a User to a Role for a specific Context.


