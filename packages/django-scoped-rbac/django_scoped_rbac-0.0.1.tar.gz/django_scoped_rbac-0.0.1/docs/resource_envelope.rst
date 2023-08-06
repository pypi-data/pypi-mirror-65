.. index:: Resource Envelope

.. _Resource Envelope:

*****************
Resource Envelope
*****************

Wrapper for a resource included in another resource. Resource Envelopes enable the
nesting of resources within other resources providing the data necessary to maintain a
coherent cache across multiple requests.

Example
=======

.. sourcecode:: json

   {
     "href": "/api/contexts/1"
     , "content-type": "application/json"
     , "last-modified": "Mon, 30 Dec 2019 15:15:15 GMT"
     , "etag": "XXXXX"
     , "context": "http://json-ld.myapp.com/contexts/context.jsonld"
     , "schema": "http://example.com/schemas/context.json#"
     , "content": {
       "id": "1"
       , "context_resource": "http://myapp.com/api/projects/1"
     }
   }

Element Definitions
===================

Resource Envelope
-----------------

.. tabularcolumns:: |l|l|L|
.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property Name
     - Value
     - Description
   * - :index:`href <pair: href; Resource Envelope>`
     - string
     - URI of the resource contained in the envelope.
   * - :index:`content-type <pair: content-type; Resource Envelope>`
     - string
     - MIME type of the resource ctonained in the envelope.
   * - :index:`last-modified <pair: last-modified; Resource Envelope>`
     - string
     - HTTP datetime for the last modified timestamp of the resource contained in the
       Resource Envelope.
   * - :index:`etag <pair: etag; Resource Envelope>`
     - string
     - The HTTP etag for the resource contained in the envelope.
   * - :index:`context <pair: context; Resource Envelope>`
     - string
     - URI of a JSON-LD context providing the RDF meaning of the data provided by the
       resource contained in the Resource Envelope.`
   * - :index:`schema <pair: schema; Resource Envelope>`
     - string
     - URI of a JSON Schema defining the JSON provided by the resource contained in the
       Resource Envelope.
   * - :index:`content <pair: content; Resource Envelope>`
     - any
     - If the ``content-type`` is ``application/json`` then the value **MUST** be a valid
       JSON value. Otherwise, the value **SHOULD** be a valid string-encoding of the
       data.
