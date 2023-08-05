"""Jinja Template Plugin.

This plugin module provides the handlers for handling jinja2 templates
and jinja2 environments containing templates.

Author:
    Martin Schorfmann
Since:
    2020-01-28
Version:
    2020-02-25
"""

import pathlib
import types
from typing import Any, Dict, List, Text

import jinja2
import markupsafe

from markdown_meta_extension.plugins.spec import (
    CallableWrapper,
    CallableHandler
)


JINJA_FILE_SUFFIXES = [
    ".htm",
    ".html",
    ".md",
    ".markdown",
    ".j2",
    ".jinja",
    ".jinja2"
]


def check_single_template_file(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper's parent path is a template file.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrapper's parent path is a template file.
    """

    template_path: pathlib.Path = callable_wrapper.parent_imported_callable()

    return any(
        suffix.lower() in JINJA_FILE_SUFFIXES\
            for suffix in template_path.suffixes
    )


def import_single_template_file(
        callable_wrapper: CallableWrapper
) -> jinja2.Template:
    """Imports the callable wrapper's single template file.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported template.
    """

    template_path: pathlib.Path = callable_wrapper.parent_imported_callable()

    template_loader = jinja2.FileSystemLoader(
        searchpath=str(template_path.parent)
    )

    # TODO: Import without loader or environment using jinja2.Template()

    template_environment = jinja2.Environment(
        loader=template_loader,
        autoescape=True
    )

    return template_environment.get_template(template_path.name)


def check_template(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper's parent import is a template.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrapper's parent import is a template.
    """

    template = callable_wrapper.parent_imported_callable()

    return isinstance(template, jinja2.Template)


def call_template(
        callable_wrapper: CallableWrapper,
        arguments: Dict[Text, Any]
) -> markupsafe.Markup:
    """Renders the template with the given arguments.

    Args:
        callable_wrapper:
            The callable wrapper around the template.
        arguments:
            The mapping of key word arguments for rendering the template.

    Returns:
        The rendered template.
    """

    if not isinstance(arguments, dict):
        arguments = dict()

    template: jinja2.Template = callable_wrapper.imported_callable

    return template.render(arguments)


def get_from_template(
        callable_wrapper: CallableWrapper,
        key: Text
) -> Any:
    """Gets the attribute from a template

    Args:
        callable_wrapper:
            The template's callable wrapper.
        key:
            The key for accessing the attribute.

    Returns:
        The accessed attribute of the template.
    """

    template: jinja2.Template = callable_wrapper.imported_callable

    if hasattr(template.module, key):  # TODO: Error handling
        return getattr(template.module, key)

    return None


def check_template_attribute(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper's parent template has the attribute.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrapper's parent template has the attribute.
    """

    attribute_name: Text = callable_wrapper.import_statement[-1]
    template: jinja2.Template = callable_wrapper.parent_imported_callable()

    # TODO: Maybe only check of import statement type or length

    return hasattr(
        template.module,
        attribute_name
    )


def import_template_attribute(
        callable_wrapper: CallableWrapper
) -> Any:
    """Imports the callable wrapper's template attribute.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported template attribute.
    """

    attribute_name: Text = callable_wrapper.import_statement[-1]
    template: jinja2.Template = callable_wrapper.parent_imported_callable()

    return getattr(
        template.module,
        attribute_name
    )


def check_template_loader_directory(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper's parent path could be a template
    directory.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrapper's parent path could be a template
        directory.
    """

    directory_path: pathlib.Path = callable_wrapper.parent_imported_callable()

    for file_suffix in JINJA_FILE_SUFFIXES:

        if directory_path.glob("*" + file_suffix):
            return True

    return False


def import_template_loader_directory(
        callable_wrapper: CallableWrapper
) -> jinja2.FileSystemLoader:
    """Imports the callable wrapper's directory template loader.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported directory template loader.
    """

    directory_path: pathlib.Path = callable_wrapper.parent_imported_callable()

    return jinja2.FileSystemLoader(
        searchpath=str(directory_path)
    )


def check_template_environment(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper's parent is a template environment.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrapper's parent is a template environment.
    """

    return isinstance(
        callable_wrapper.parent_imported_callable(),
        jinja2.BaseLoader
    )


def import_template_environment(
        callable_wrapper: CallableWrapper
) -> jinja2.Environment:
    """Imports the callable wrapper's template environment using
    an existing loader.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported template environment.
    """

    loader: jinja2.BaseLoader = callable_wrapper.parent_imported_callable()

    template_environment = jinja2.Environment(
        loader=loader,
        autoescape=True
    )

    return template_environment


def check_template_from_environment(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper's parent template environment
    can be used to get the template.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrapper's parent template environment
        can be used to get the template.
    """

    environment: jinja2.Environment = callable_wrapper.parent_imported_callable()

    # TODO: Find better solution
    if len(callable_wrapper.import_statement) < 2:
        return False

    template_path = pathlib.Path(callable_wrapper.import_statement[1])

    return bool(environment.get_template(str(template_path)))


def import_template_from_environment(
        callable_wrapper: CallableWrapper
) -> jinja2.Environment:
    """Imports the callable wrapper's environment template

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported template.
    """

    environment: jinja2.Environment = callable_wrapper.parent_imported_callable()

    # TODO: Find better solution
    template_path = pathlib.Path(callable_wrapper.import_statement[1])

    return environment.get_template(str(template_path))


JINJA_TEMPLATE_FILE_HANDLER = CallableHandler(
    name="jinja_template_file",
    requires=["file_system_file"],
    check_function=check_single_template_file,
    import_function=import_single_template_file,
    call_function=None,
    get_function=None
)

JINJA_LOADER_DIRECTORY_HANDLER = CallableHandler(
    name="jinja_loader_directory",
    requires=["file_system_directory"],
    check_function=check_template_loader_directory,
    import_function=import_template_loader_directory,
    call_function=None,
    get_function=None
)

JINJA_ENVIRONMENT_HANDLER = CallableHandler(
    name="jinja_environment",
    requires=["jinja_loader_directory"],
    check_function=check_template_environment,
    import_function=import_template_environment,
    call_function=None,
    get_function=None
)

JINJA_TEMPLATE_ENVIRONMENT_HANDLER = CallableHandler(
    name="jinja_template_environment",
    requires=["jinja_environment"],
    check_function=check_template_from_environment,
    import_function=import_template_from_environment,
    call_function=None,
    get_function=None
)

JINJA_TEMPLATE_HANDLER = CallableHandler(
    name="jinja_template",
    requires=["jinja_template_file", "jinja_template_environment"],  # TODO: Further requires
    check_function=check_template,
    import_function=None,
    call_function=call_template,
    get_function=get_from_template # TODO: Use getattr(template.module, "macro")
)

JINJA_TEMPLATE_ATTRIBUTE_HANDLER = CallableHandler(
    name="jinja_template_attribute",
    requires=["jinja_template"],
    check_function=check_template_attribute,
    import_function=import_template_attribute,
    call_function=None,
    get_function=None
)


def get_callable_handler() -> List[CallableHandler]:
    """Returns the jinja2 templates related callable handlers."""

    return [
        JINJA_TEMPLATE_FILE_HANDLER,
        JINJA_LOADER_DIRECTORY_HANDLER,
        JINJA_ENVIRONMENT_HANDLER,
        JINJA_TEMPLATE_ENVIRONMENT_HANDLER,
        JINJA_TEMPLATE_HANDLER,
        JINJA_TEMPLATE_ATTRIBUTE_HANDLER,
    ]
