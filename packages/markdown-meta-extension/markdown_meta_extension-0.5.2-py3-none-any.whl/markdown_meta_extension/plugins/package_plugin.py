"""Package Handler Plugin.

This plugin module provides the handler for handling import statements
for (installed) Python packages.

Author:
    Martin Schorfmann
Since:
    2020-01-28
Version:
    2020-02-25
"""

import importlib
import types

from markdown_meta_extension.plugins.spec import (
    CallableWrapper,
    CallableHandler
)

def check_package_path(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper imports a Python package.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        Whether the callable wrapper imports a Python package.
    """

    try:
        return bool(
            importlib.util.find_spec(
                callable_wrapper.import_statement[0]
            )
        )
    except ValueError:
        return False

def import_package(
        callable_wrapper: CallableWrapper
) -> types.ModuleType:
    """Imports the callable wrapper's Python package.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported Python module.
    """
    package_path = callable_wrapper.import_statement[0]

    try:
        imported_module = importlib.import_module(package_path)
    except ImportError:  # TODO: Error handling
        imported_module = None

    return imported_module


PACKAGE_HANDLER = CallableHandler(
    name="package",
    requires=None,
    check_function=check_package_path,
    import_function=import_package
)

def get_callable_plugin() -> CallableHandler:
    """Returns the callable handler for importing Python packages."""
    return PACKAGE_HANDLER
