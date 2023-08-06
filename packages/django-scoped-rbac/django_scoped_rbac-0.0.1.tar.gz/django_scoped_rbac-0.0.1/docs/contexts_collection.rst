.. index:: Contexts Collection

.. _Contexts Collection:

*******************
Contexts Collection
*******************

A *Contexts Collection* is a resource containing a listing of :ref:`Context Resource`
defined in the application.

IRI
===

``http://scoped-rbac.github.io/rdf/ContextsCollection``

Example
=======

.. sourcecode:: json

   {
     "contexts": [
       {
         "href": "/api/contexts/1"
         , "content-type": "application/json"
         , "last-modified": "Mon, 30 Dec 2019 15:15:15 GMT"
         , "etag": "XXXXX"
         , "context": "http://json-ld.myapp.com/contexts/context.jsonld"
         , "schema": "http://example.com/schemas/user.json#"
         , "content": {
           "id": "1"
           , "context_resource": "http://myapp.com/api/projects/1"
         }
       }
       , {
         "href": "/api/contexts/2"
         , "content-type": "application/json"
         , "last-modified": "Mon, 30 Dec 2019 15:15:15 GMT"
         , "etag": "XXXXX"
         , "context": "http://json-ld.myapp.com/contexts/context.jsonld"
         , "schema": "http://example.com/schemas/user.json#"
         , "content": {
           "id": "2"
           , "context_resource": "http://myapp.com/api/projects/2"
         }
       }
     ]
   }

..


Element Definition
==================

Contexts Collection
-------------------

.. tabularcolumns:: |l|l|L|
.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property Name
     - Value
     - Description
   * - :index:`contexts <pair: contexts; Contexts Collection>`
     - list
     - List of :ref:`Context Resource`.

RDF Context
===========

.. sourcecode:: json

   {
     "contexts": {
       "@id": "http://scoped-rbac.github.io/rdf/ResourceEnvelope"
       , "contents": "http://scoped-rbac.github.io/rdf/ContextResource"
     }
   }

.. index::
   pair: GET; Contexts Collection
   pair: HEAD; Contexts Collection

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
       response entity **MUST** be provided and **MUST** be a
       :ref:`Context Collection`.
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
     - No :ref:`Contexts Collection` could be found for the requested URL.

Example
-------

Request
^^^^^^^

.. sourcecode:: http

   GET /api/contexts/ HTTP/1.1
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
     "contexts": [
       {
         "href": "/api/contexts/1"
         , "content-type": "application/json"
         , "last-modified": "Mon, 30 Dec 2019 15:15:15 GMT"
         , "etag": "XXXXX"
         , "context": "http://json-ld.myapp.com/contexts/context.jsonld"
         , "schema": "http://example.com/schemas/user.json#"
         , "content": {
           "id": "1"
           , "context_resource": "http://myapp.com/api/projects/1"
         }
       }
       , {
         "href": "/api/contexts/2"
         , "content-type": "application/json"
         , "last-modified": "Mon, 30 Dec 2019 15:15:15 GMT"
         , "etag": "XXXXX"
         , "context": "http://json-ld.myapp.com/contexts/context.jsonld"
         , "schema": "http://example.com/schemas/user.json#"
         , "content": {
           "id": "2"
           , "context_resource": "http://myapp.com/api/projects/2"
         }
       }
     ]
   }

.. index:: pair: PUT; Contexts Collection

HTTP PUT
========

HTTP PUT is not supported. The server **MUST** respond with
``405 Method Not Allowed``.

.. index:: pair: POST; Contexts Collection

HTTP POST
=========

HTTP POST is not supported. The server **MUST** respond with
``405 Method Not Allowed``.

.. index:: pair: DELETE; Contexts Collection

HTTP DELETE
===========

HTTP DELETE is not supported. The server **MUST** respond with
``405 Method Not Allowed``.
