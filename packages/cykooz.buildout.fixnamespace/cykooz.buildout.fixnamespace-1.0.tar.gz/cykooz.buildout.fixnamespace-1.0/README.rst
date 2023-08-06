****************************
cykooz.buildout.fixnamespace
****************************

This buildout extension changes value of NAMESPACE_PACKAGE_INIT
constant from ``setuptools``. This value used to fix namespace packages
installed from wheels (https://github.com/pypa/setuptools/issues/2069).

Extension replace value of NAMESPACE_PACKAGE_INIT with code:

.. code-block:: python

    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

Minimal usage example::

    [buildout]
    extensions = cykooz.buildout.fix_namespace

