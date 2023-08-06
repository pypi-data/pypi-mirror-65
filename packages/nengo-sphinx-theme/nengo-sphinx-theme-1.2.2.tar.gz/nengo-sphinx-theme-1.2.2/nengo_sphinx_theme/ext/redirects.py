"""
This extension generates pages to redirect a URL from an old location to a new one.
These pages will only be generated when building with the HTML builder.

This extension can be enabled by adding ``"nengo_sphinx_theme.ext.redirects"``
to the ``extensions`` list in ``conf.py``.

This extension adds a new configuration option to ``conf.py`` called
``html_redirects``. ``html_redirects`` is a list of tuples, where each tuple has
two elements: the original location and the new location. Locations are usually
strings pointing to HTML files, but the new location can also be an anchor link
or some other valid URL.

As an example, suppose we rename a file from ``user_guide.rst`` to ``user-guide.rst``,
and move the content on ``dev_guide.rst`` to a section in ``user-guide.rst``.
The redirects might look like this::

   html_redirects = [
       ("user_guide.html", "user-guide.html"),
       ("dev_guide.html", "user-guide.html#developers")
   ]

"""

import errno
import os
from textwrap import dedent


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


out_html = dedent(
    """\
    <!DOCTYPE html>
    <html>
      <head><title>This page has moved</title></head>
      <body>
        <script type="text/javascript">
          window.location.replace("{0}");
        </script>
        <noscript>
          <meta http-equiv="refresh" content="0; url={0}">
        </noscript>
      </body>
    </html>
    """
).rstrip(" ")


def setup(app):
    def redirect_pages(app, docname):
        if app.builder.name == "html":
            for src, dst in app.config.html_redirects:
                srcfile = os.path.join(app.outdir, src)
                dsturl = "/".join([".." for _ in range(src.count("/"))] + [dst])
                mkdir_p(os.path.dirname(srcfile))
                with open(srcfile, "w") as fp:
                    fp.write(out_html.format(dsturl))

    app.add_config_value("html_redirects", [], "")
    app.connect("build-finished", redirect_pages)
