***************
Release History
***************

.. Changelog entries should follow this format:

   version (release date)
   ======================

   **section**

   - One-line description of change (link to Github issue/PR)

.. Changes should be organized in one of several sections:

   - Added
   - Changed
   - Deprecated
   - Removed
   - Fixed

1.2.2 (April 14, 2020)
======================

**Fixed**

- ``nengo_sphinx_theme.ext.resolvedefaults`` will not touch signatures unless they
  contain a ``Default`` value.
  (`#54 <https://github.com/nengo/nengo-sphinx-theme/pull/54>`__)

1.2.1 (March 19, 2019)
======================

**Added**

- Added the ``autoautosummary_change_modules`` config option to
  ``nengo_sphinx_theme.ext.autoautosummary``, which allows classes/functions
  documented with ``autoautosummary`` or ``automodule`` to be moved to a different
  nominal namespace. (`#52 <https://github.com/nengo/nengo-sphinx-theme/pull/52>`__)
- Added ``nengo_sphinx_theme.ext.backoff``, which monkeypatches the Sphinx
  HTTP request functionality to add exponential backoff.
  (`#52 <https://github.com/nengo/nengo-sphinx-theme/pull/52>`__)

1.2.0 (November 14, 2019)
=========================

**Added**

- Added an extension to handle redirecting old HTML pages to new ones.
  (`#48 <https://github.com/nengo/nengo-sphinx-theme/pull/48>`__)

1.1.0 (November 5, 2019)
========================

**Added**

- Added an extension with the ``AutoAutoSummary`` directive, which will
  automatically generate Sphinx AutoSummaries for modules and classes.
  (`#45 <https://github.com/nengo/nengo-sphinx-theme/pull/45>`__)

1.0.3 (September 13, 2019)
==========================

**Changed**

- Updated header and footer to match changes to nengo.ai.
  (`#41 <https://github.com/nengo/nengo-sphinx-theme/pull/41>`__)

1.0.2 (August 5, 2019)
======================

**Fixed**

- Fixed the search box, which was hanging for many search terms.
  (`#28 <https://github.com/nengo/nengo-sphinx-theme/issues/28>`__,
  `#39 <https://github.com/nengo/nengo-sphinx-theme/pull/39>`__)

1.0.1 (July 16, 2019)
=====================

**Changed**

- Fixed a missing divider in the documentation drop-down menu.

1.0.0 (July 16, 2019)
=====================

**Changed**

- The look-and-feel of the theme was completely redone.
  (`#35 <https://github.com/nengo/nengo-sphinx-theme/pull/35>`__)
- This project is now licensed with the Nengo license.
  (`#35 <https://github.com/nengo/nengo-sphinx-theme/pull/35>`__)

0.12.0 (May 29, 2019)
=====================

**Added**

- Added ``nengo_sphinx_theme.ext.resolvedefaults`` extension that will
  automatically fill in the value of ``nengo.Default`` values in
  ``__init__`` signatures.
  (`#33 <https://github.com/nengo/nengo-sphinx-theme/pull/33>`_)

0.11.0 (May 20, 2019)
=====================

**Added**

- Added a theme option to enable Google Analytics tracking by
  providing an ID.
  (`#30 <https://github.com/nengo/nengo-sphinx-theme/pull/30>`__)

**Fixed**

- Fixed an issue in which the dropdown overlay prevented clicks
  after it had been hidden from mousing outside of it.
  (`#29 <https://github.com/nengo/nengo-sphinx-theme/pull/29>`__)

0.10.0 (March 30, 2019)
=======================

**Fixed**

- Added ``body`` class to main div for compatibility with sphinx 2.0.
  (`#26 <https://github.com/nengo/nengo-sphinx-theme/pull/26>`__)

0.9.0 (March 25, 2019)
======================

**Added**

- Added search box to sidebar.
  (`#25 <https://github.com/nengo/nengo-sphinx-theme/pull/25>`__)
