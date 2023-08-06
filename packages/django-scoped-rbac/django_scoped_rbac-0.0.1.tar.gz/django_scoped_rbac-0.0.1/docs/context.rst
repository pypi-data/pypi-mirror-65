.. index:: Context Resource

.. _Context Resource:

****************
Context Resource
****************

A *Context* resource wraps another resource as a general context for Django Scoped RBAC.

IRI
===

``http://scoped-rbac.github.io/rdf/Context``

Example
=======

.. sourcecode:: json

   {
     "id": "1"
     , "context_resource": "http://myapp.com/api/projects/1"
   }

Element Definitions
===================

Context Resource
----------------

.. tabularcolumns:: |l|l|L|
.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property Name
     - Value
     - Description
   * - :index:`id <pair: id; Context Resource>`
     - string
     - Unique identifier for the *Context*
   * - :index:`context_resource <pair: context_resource; Context Resource>`
     - string
     - Hyperlink to the wrapped resource for this generalized *Context*.

.. index:: pair: RDF Context; Context Resource

RDF Context
===========

.. sourcecode:: json

   {
     "id": "@id"
     , "context_resource": "http://scoped-rbac.github.io/rdf/2019/ContextResourceHref"
   }

.. index::
   pair: GET; Context Resource
   pair: HEAD; Context Resource

HTTP GET/HEAD
=============

Response Codes
--------------

.. tabularcolumns:: |l|L|
.. list-table::
   :widths: 20 80
   :header-rows: 1
   
   * - Status Code
     - Description
   * - 200 OK
     - The request was valid, authorized, and executed successfully. The
       response entity **MUST** be provided and **MUST** be an
       :ref:`OrganizationResource`.
   * - 304 Not Modified
     - If the client has performed a conditional GET or HEAD request and the
       resource hasn't been modified the server **SHOULD** respond with this
       status code.
   * - 401 Unauthorized
     - The client and/or user has not been authenticated or the provided
       :ref:`SessionAccessToken` has expired.
   * - 403 Forbidden
     - The client and/or the user is not authorized to GET the requested
       resource.
   * - 404 Not Found
     - No :ref:`OrganizationResource` could be found for the requested URL.

Example
-------

Request
^^^^^^^

.. sourcecode:: http

   GET /api/contexts/42 HTTP/1.1
   Host: myapp.com
   Accept: application/json

Response
^^^^^^^^

.. sourcecode:: http

   HTTP/1.1 200 OK
   Date: Mon, 30 Dec 2019 15:15:15 GMT
   Content-Length: XXXXX
   Content-Type: application/json
   Last-Modified: Mon, 30 Jul 2019 14:15:15 GMT
   ETag: "XXXX"
   
   {
      "id": "1"
      , "context_resource": "/api/projects/1"
   }

.. index:: pair: PUT; Context Resource

HTTP PUT
========

HTTP PUT is not supported. The server **MUST** respond with
``405 Method Not Allowed``.

.. index:: pair: POST; Context Resource

HTTP POST
=========

HTTP POST is not supported. The server **MUST** respond with
``405 Method Not Allowed``.

.. index:: pair: DELETE; Context Resource

HTTP DELETE
===========

HTTP DELETE is not supported. The server **MUST** respond with
``405 Method Not Allowed``.
