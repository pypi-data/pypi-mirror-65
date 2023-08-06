"""
This extension automatically generates AutoSummaries for modules/classes.

This extension can be enabled by adding ``"nengo_sphinx_theme.ext.autoautosummary"``
to the ``extensions`` list in ``conf.py``.
"""

import inspect

from docutils.parsers.rst import directives
import sphinx.ext.autodoc as autodoc
import sphinx.ext.autosummary as autosummary

# We import nengo_sphinx_theme here to test the issue that
# `patch_autosummary_import_by_name` fixes.

import nengo_sphinx_theme  # pylint: disable=unused-import


# should be ignored
a_test_attribute = None


def a_test_function():
    """This is a test function."""


class TestClass:
    """This is a test class."""

    # should be ignored
    an_attribute = None

    def __init__(self):
        """This is the init method."""

    def a_method(self):
        """This is a method."""

    @staticmethod
    def a_static_method():
        """This is a static method."""

    def _a_private_method(self):
        """A private method."""

    def _another_private_method(self):
        """This method will be manually added."""


class AutoAutoSummary(autosummary.Autosummary):
    """
    Automatically generates a summary for a class or module.

    For classes this adds a summary for all methods.

    For modules this adds a summary for all classes/functions.
    """

    option_spec = {
        **autosummary.Autosummary.option_spec,
        "exclude-members": directives.unchanged,
    }

    required_arguments = 1

    def get_members(self, obj):
        if inspect.isclass(obj):
            module_name = obj.__module__

            def filter(x):
                return inspect.isroutine(x)

        elif inspect.ismodule(obj):
            module_name = obj.__name__

            def filter(x):
                return inspect.isclass(x) or inspect.isfunction(x)

        else:
            raise TypeError(
                "AutoAutoSummary only works with classes or modules (got %s)"
                % type(obj)
            )

        excluded = [
            x.strip() for x in self.options.get("exclude-members", "").split(",")
        ]

        items = []
        # note: we use __dict__ because it preserves the order of attribute definitions
        # (in python >= 3.6)
        for name in obj.__dict__:
            if not (name.startswith("_") or name in excluded):
                attr = getattr(obj, name)

                if filter(attr) and attr.__module__ == module_name:
                    items.append(name)

        return items

    def run(self):
        fullname = str(self.arguments[0])
        (module_name, obj_name) = fullname.rsplit(".", 1)
        mod = __import__(module_name, globals(), locals(), [obj_name])
        obj = getattr(mod, obj_name)

        # cast from "ViewList" to regular list
        self.content = list(self.content)

        # add all members of object to the autosummary (with renaming)
        for item in self.get_members(obj):
            if inspect.ismodule(obj):
                # the renaming is on the level of module objects (e.g., classes),
                # so add the object name before doing the name lookup
                item_name = "%s.%s" % (fullname, item)

                # look up any renaming, defaulting to the current module name
                renamed_module = self.env.config["autoautosummary_change_modules"].get(
                    item_name, fullname
                )

                # add the item name to the (renamed) module
                member_name = "%s.%s" % (renamed_module, item)
            else:
                # obj is already a renameable object (e.g. a class), so we're just
                # looking up based on fullname
                item_name = fullname

                # default to module_name (since the output of rename lookup should be
                # a module, whereas fullname would be a class)
                renamed_module = self.env.config["autoautosummary_change_modules"].get(
                    item_name, module_name
                )

                # add class and member name to renamed module
                member_name = "%s.%s.%s" % (renamed_module, obj_name, item)

            self.content.append(member_name)

        return super(AutoAutoSummary, self).run()


def patch_autosummary_import_by_name():
    """Monkeypatch a function in autosummary to disallow module cycles"""

    orig_f = autosummary.import_by_name

    def import_by_name(name, prefixes):
        # We currently do not support prefixes, because they can cause cycles. If we
        # need this in the future, we can go back to filtering problematic prefixes.
        prefixes = [None]
        return orig_f(name, prefixes)

    autosummary.import_by_name = import_by_name


class RenameMixin:
    """Mixin for adding renaming functionality to autodocumenters."""

    def add_directive_header(self, sig):
        """
        Change the modname so that ``:module: renamed_module`` is added in the header.
        """

        modname = self.modname

        if self.objtype == "method":
            # drop method name (since renames are by class)
            lookup_name = ".".join(self.fullname.split(".")[:-1])
        else:
            lookup_name = self.fullname

        self.modname = self.env.config["autoautosummary_change_modules"].get(
            lookup_name, modname
        )

        super().add_directive_header(sig)

        # set the modname back to the "true" modname, since other parts of the
        # rendering process may depend on that
        self.modname = modname


class RenameClassDocumenter(RenameMixin, autodoc.ClassDocumenter):
    """Class autodocumenter with optional renaming."""


class RenameFunctionDocumenter(RenameMixin, autodoc.FunctionDocumenter):
    """Function autodocumenter with optional renaming."""


class RenameExceptionDocumenter(RenameMixin, autodoc.ExceptionDocumenter):
    """Exception autodocumenter with optional renaming."""


class RenameDecoratorDocumenter(RenameMixin, autodoc.DecoratorDocumenter):
    """Decorator autodocumenter with optional renaming."""


class RenameMethodDocumenter(RenameMixin, autodoc.MethodDocumenter):
    """Method autodocumenter with optional renaming."""


def setup(app):
    patch_autosummary_import_by_name()
    app.add_directive("autoautosummary", AutoAutoSummary)

    app.add_config_value("autoautosummary_change_modules", {}, "")

    def swap_config(app, config):
        # change from mod: items to {item: mod, item: mod, ...}
        swapped = {}
        for mod, items in config["autoautosummary_change_modules"].items():
            swapped.update((x, mod) for x in items)
        config["autoautosummary_change_modules"] = swapped

    app.connect("config-inited", swap_config)

    app.add_autodocumenter(RenameClassDocumenter, override=True)
    app.add_autodocumenter(RenameFunctionDocumenter, override=True)
    app.add_autodocumenter(RenameExceptionDocumenter, override=True)
    app.add_autodocumenter(RenameDecoratorDocumenter, override=True)
    app.add_autodocumenter(RenameMethodDocumenter, override=True)
