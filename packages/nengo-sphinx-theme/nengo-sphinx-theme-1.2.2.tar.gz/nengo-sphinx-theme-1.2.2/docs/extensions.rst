***************
Extension tests
***************

This page tests the extensions that are part of this theme.

Versioning
==========

This extension is always used
if ``releases`` are passed to the Sphinx build.

:doc:`deeply/nested/testing/page`
versioned links work properly.

Default resolution
==================

This extension can be enabled by adding
``"nengo_sphinx_theme.ext.resolvedefaults"``
to the ``extensions`` list in ``conf.py``.

Autodoc with default resolution:

.. autoclass:: nengo_sphinx_theme.ext.resolvedefaults.TestClass

AutoAutoSummary
===============

.. automodule:: nengo_sphinx_theme.ext.autoautosummary
   :exclude-members: TestClass

   .. autoautosummary:: nengo_sphinx_theme.ext.autoautosummary
      :exclude-members: setup

.. autoclass:: nengo_sphinx_theme.ext.autoautosummary.TestClass
   :private-members:

   .. autoautosummary:: nengo_sphinx_theme.ext.autoautosummary.TestClass
      :nosignatures:

      nengo_sphinx_theme.ext.renamed_autoautosummary.TestClass._another_private_method

Redirects
=========

.. automodule:: nengo_sphinx_theme.ext.redirects
   :no-members:

The following page should redirect to the
`deeply nested testing page <redirect/to/nested-page.html>`_.

Backoff
=======

.. automodule:: nengo_sphinx_theme.ext.backoff
