"""Module Handlers Plugin.

This plugin module provides the handlers for handling already imported Python
modules and using their contents like functions, classes or objects.

Author:
    Martin Schorfmann
Since:
    2020-01-28
Version:
    2020-02-25
"""

import inspect
import types
from typing import Any, List

from markdown_meta_extension.plugins.spec import (
    CallableWrapper,
    CallableHandler
)


ATTRIBUTE_SEPARATOR = "."


def check_module(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrappers current import is a Python module.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrappers current import is a Python module.
    """

    imported_callable = callable_wrapper.parent_imported_callable()

    return isinstance(imported_callable, types.ModuleType)


def check_type(
        callable_wrapper: CallableWrapper,
        type_checker: type
) -> bool:
    """Checks whether the callable wrappers current import is of the given type.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.
        type_checker:
            The type to check against.

    Returns:
        Whether the callable wrappers current import is of the given type.
    """

    return isinstance(
        callable_wrapper.parent_imported_callable,
        type_checker
    )


def check_type_function(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrappers current import is a function.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrappers current import is a function.
    """

    return check_type(callable_wrapper, types.FunctionType)


def check_type_class(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrappers current import is a class.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrappers current import is a class.
    """

    return inspect.isclass(
        callable_wrapper.parent_imported_callable()
    )


def check_type_object(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrappers current import is an object.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrappers current import is an object.
    """

    return check_type(callable_wrapper, object)


def check_type_method(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrappers current import is a method.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrappers current import is a method.
    """

    return check_type(callable_wrapper, types.MethodType)


def import_module_attribute(
        callable_wrapper: CallableWrapper
) -> Any:
    """Imports the callable wrapper's module attribute

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported module attribute.
    """

    attribute_paths = callable_wrapper.import_statement[1:]
    attribute_names = list()

    for attribute_path in attribute_paths:
        attribute_names = attribute_names\
            + attribute_path.split(ATTRIBUTE_SEPARATOR)

    imported_callable = callable_wrapper.parent_imported_callable()

    for attribute_name in attribute_names:
        imported_callable = getattr(
            imported_callable,
            attribute_name
        )

    return imported_callable

MODULE_ATTRIBUTE_HANDLER = CallableHandler(
    name="module_attribute",
    requires=["file_system_module", "package"],
    check_function=check_module,
    import_function=import_module_attribute,
    call_function=None,
    get_function=None
)

MODULE_FUNCTION_HANDLER = CallableHandler(
    name="function",
    requires=["module_attribute"],
    check_function=check_type_function,
    import_function=None,
    call_function=None,
    get_function=None
)

MODULE_CLASS_HANDLER = CallableHandler(
    name="class",
    requires=["module_attribute"],
    check_function=check_type_class,
    import_function=None,
    call_function=None,
    get_function=None
)

MODULE_OBJECT_HANDLER = CallableHandler(
    name="object",
    requires=["module_attribute"],
    check_function=check_type_object,
    import_function=None,
    call_function=None,
    get_function=None
)

MODULE_METHOD_HANDLER = CallableHandler(
    name="method",
    requires=["module_attribute"],
    check_function=check_type_method,
    import_function=None,
    call_function=None,
    get_function=None
)


def get_callable_handler() -> List[CallableHandler]:
    """Returns the module and module attribute related callable handlers."""

    return [
        MODULE_ATTRIBUTE_HANDLER,
        MODULE_FUNCTION_HANDLER,
        MODULE_CLASS_HANDLER,
        MODULE_OBJECT_HANDLER,
        MODULE_METHOD_HANDLER
    ]
