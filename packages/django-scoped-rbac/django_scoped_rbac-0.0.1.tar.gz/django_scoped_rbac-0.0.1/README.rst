==================
django_scoped_rbac
==================

.. image:: https://github.com/Quansight/django-scoped-rbac/workflows/Django%20CI/badge.svg
   :target: Django CI

A rich and flexible Django application for role-based access control within
distinct access control scopes supporting Django Rest Framework.

Motivation
----------

* Support multiple security contexts within an application, rather than having the
  application serve as the single security context.
* Support a model of security context that can be enforced at the query level within the
  database. For example - list all resources within the contexts the user is authorized
  to list resources.
* Support assignment of roles within a security context.
* Support an extensible mechanism for conditional policy expressions for permissions.
* Support a JSON representation of the total permissions granted to a user for all
  security contexts that can be shared with browser and other clients to enable
  permissions-informed disclosure UI and UX


Support multiple security contexts within an application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most RBAC systems provide a simple permission model to answer permissions. For example,
is the user authorized to POST a comment. In an application that supports multiple
security contexts the relevant context is an additional parameter required to determine
if the user is authorised; that is is the user authorized to POST a comment to this
project vs another project. A user may be authorized to POST a comment to one project,
but not another.


Support for security contexts at the query level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If every object has a security context property it's possible to always secure the
queries executed for a user request by adding the user's authorized security contexts as
an "IN" condition restricting the scope of the query.


Support assignment of roles within a security context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most RBAC systems a user is assigned a role that is applicable across the entire
application. For example, a user may have a `Commenter` role granting the user the
permission to post comments anywhere comments may be posted within the application. An
application that supports the assignment of a role within the scope of a specific
security context can restrict the assignment of the `Commenter` role to specific areas
of an application. For example, a user may be assigned the `Commenter` role in `Project
1` but not `Project 2`.


Support an extensible mechanism for conditional policy expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another limitation of most RBAC systems is the simplicity of their permissions - you are
either authorized to perform an action or not. Supporting an extensible mechanism for
conditional policy expression means that a permission may be conditionally granted
dependant upon a variety of factors. For example, you may be granted the permission to
comment within a project only when a target resource within the scope of that project is
"open for community comments" vs "open for drafter comments".


Support JSON representation of total permissions granted
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a user has permission to perform an action, such as update a resource, it should be
possible for a client to determine that this is the case and be able to decide whether
to disclose editing capabilty for the resource to the user. That is, if I'm not
authorised to edit a resource the UI shouldn't offer me the opportunity to edit the
resource.

Providing a JSON representation of the user's total permissions, and a Javascript
implementation of the permissions policy engine, can provide a much richer user
experience.


Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
