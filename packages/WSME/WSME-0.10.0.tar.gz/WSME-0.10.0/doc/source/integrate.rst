Integrating with a Framework
============================

General considerations
----------------------

Using WSME within another framework providing its own REST capabilities is
generally done by using a specific decorator to declare the function signature,
in addition to the framework's own way of declaring exposed functions.

This decorator can have two different names depending on the adapter.

``@wsexpose``
    This decorator will declare the function signature *and*
    take care of calling the adequate decorators of the framework.

    Generally this decorator is provided for frameworks that use
    object-dispatch controllers, such as :ref:`adapter-pecan`.

``@signature``
    This decorator only sets the function signature and returns a function
    that can be used by the host framework as a REST request target.

    Generally this decorator is provided for frameworks that expect functions
    taking a request object as a single parameter and returning a response
    object. This is the case for :ref:`adapter-flask`.

If you want to enable additional protocols, you will need to
mount a :class:`WSRoot` instance somewhere in the application, generally
``/ws``. This subpath will then handle the additional protocols. In a future
version, a WSGI middleware will probably play this role.

.. note::

    Not all the adapters are at the same level of maturity.

WSGI Application
----------------

The :func:`wsme.WSRoot.wsgiapp` function of WSRoot returns a WSGI
application.

Example
~~~~~~~

The following example assumes the REST protocol will be entirely handled by
WSME, which is the case if you write a WSME standalone application.

.. code-block:: python

    from wsme import WSRoot, expose


    class MyRoot(WSRoot):
        @expose(unicode)
        def helloworld(self):
            return u"Hello World !"

    root = MyRoot(protocols=['restjson'])
    application = root.wsgiapp()


.. _adapter-flask:

Flask
-----

    *"Flask is a microframework for Python based on Werkzeug, Jinja 2 and good
    intentions. And before you ask: It's BSD licensed! "*


.. warning::

    Flask support is limited to function signature handling. It does not
    support additional protocols. This is a temporary limitation, if you have
    needs on that matter please tell us at python-wsme@googlegroups.com.


:mod:`wsmeext.flask` -- Flask adapter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: wsmeext.flask

.. function:: signature(return_type, \*arg_types, \*\*options)

    See @\ :func:`signature` for parameters documentation.

    Can be used on a function before routing it with flask.

Example
~~~~~~~

.. code-block:: python

    from wsmeext.flask import signature

    @app.route('/multiply')
    @signature(int, int, int)
    def multiply(a, b):
        return a * b

.. _adapter-pecan:

Pecan
-----

    *"*\ Pecan_ *was created to fill a void in the Python web-framework world –
    a very lightweight framework that provides object-dispatch style routing.
    Pecan does not aim to be a "full stack" framework, and therefore includes
    no out of the box support for things like sessions or databases. Pecan
    instead focuses on HTTP itself."*

.. warning::

    A pecan application is not able to mount another WSGI application on a
    subpath. For that reason, additional protocols are not supported for now,
    until WSME provides a middleware that can do the same as a mounted
    WSRoot.

:mod:`wsmeext.pecan` -- Pecan adapter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: wsmeext.pecan

.. function:: wsexpose(return_type, \*arg_types, \*\*options)

    See @\ :func:`signature` for parameters documentation.

    Can be used on any function of a pecan
    `RestController <http://pecan.readthedocs.org/en/latest/rest.html>`_
    instead of the expose decorator from Pecan.

Configuration
~~~~~~~~~~~~~

WSME can be configured through the application configation, by adding a 'wsme'
configuration entry in ``config.py``:

.. code-block:: python

    wsme = {
        'debug': True
    }

Valid configuration variables are :

-   ``'debug'``: Whether or not to include exception tracebacks in the returned
    server-side errors.

Example
~~~~~~~

The `example <http://pecan.readthedocs.org/en/latest/rest.html#nesting-restcontroller>`_ from the Pecan documentation becomes:

.. code-block:: python

    from wsmeext.pecan import wsexpose

    class BooksController(RestController):
        @wsexpose(Book, int, int)
        def get(self, author_id, id):
            # ..

        @wsexpose(Book, int, int, body=Book)
        def put(self, author_id, id, book):
            # ..

    class AuthorsController(RestController):
            books = BooksController()

.. _Pecan: http://pecanpy.org/
