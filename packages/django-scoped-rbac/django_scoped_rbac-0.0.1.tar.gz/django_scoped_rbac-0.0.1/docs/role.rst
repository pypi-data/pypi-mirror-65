.. index:: Role Resource

.. _Role Resource:

*************
Role Resource
*************

A *Role Resource* defines a set of permissions.

IRI
===

``http://scoped-rbac.github.io/rdf/Role``

Example
=======

.. sourcecode:: json

   {
     "id": "1"
     , "displayname": "Editor of A"
     , "description": "Users with permission to CRUD A resources."
     , "policy": {
       "GET": {
         "http://example.com/rdf/ResourceTypeA": true
         , "http://example.com/rdf/ResourceTypeB": true
       }
       , "PUT": {
         "http://example.com/rdf/ResourceTypeA": true
       }
       , "POST": {
         "http://example.com/rdf/ResourceTypeA": true
       }
       , "DELETE": {
         "http://example.com/rdf/ResourceTypeA": true
       }
     }
   }

..

Element Definitions
===================

Role Resource
-------------

.. tabularcolumns:: |l|l|L|
.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Value
     - Description
   * - :index:`id <pair: id; Role Resource>`
     - string
     - Unique ID for the Role Resource.
   * - :index:`displayname <pair: displayname; Role Resource>`
     - string
     - A short name to display when listing the Role Resource.
   * - :index:`description <pair: description; Role Resource>`
     - string
     - A longer and more detailed description of the role defined by the Role Resource.
   * - :index:`policy <pair: policy; Role Resource>`
     - :ref:`Policy`
     - The policy defining the role.

.. _Policy:

Policy
------

.. tabularcolumns:: |l|l|L|
.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Value
     - Description
   * - *Action*
     - :ref:`ActionPolicy`
     - A *Policy* is indexed by *Actions* that are supported by the application.

.. _ActionPolicy:

ActionPolicy
------------

.. tabularcolumns:: |l|l|L|
.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Value
     - Description
   * - *Resource-Type IRI*
     - bool or :ref:`PolicyExpression`
     - An *ActionPolicy* is indexed by *Rsource-Type IRIs*.

.. _PolicyExpression:

PolicyExpression
----------------

A *PolicyExpression* is an object that captures a conditional expression that must
evaluate to true for the associated action to be permitted for the authorized user.

*More details to come*

.. tabularcolumns:: |l|l|L|
.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Value
     - Description
