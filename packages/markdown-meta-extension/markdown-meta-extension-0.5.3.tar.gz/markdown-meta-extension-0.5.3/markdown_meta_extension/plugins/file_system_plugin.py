"""File System Handlers Plugin.

This plugin module provides the handlers for handling file paths in import
statements.

Author:
    Martin Schorfmann
Since:
    2020-01-26
Version:
    2020-03-14
"""

import importlib
import pathlib
import types
from typing import List, Text

import pathvalidate

from markdown_meta_extension.plugins.spec import (
    CallableWrapper,
    CallableHandler
)


PYTHON_FILE_SUFFIX: Text = ".py"


def check_file_system_path(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks for a file system path.

    Args:
        callable_wrapper:
            The callable wrapper to get checked.

    Returns:
        Whether the checked callable wrapper has a valid and existing path.
    """

    file_system_path = pathlib.Path(
        callable_wrapper.import_statement[0]
    )

    try:
        pathvalidate.validate_filepath(file_system_path)
    except pathvalidate.ValidationError:
        return False

    if not file_system_path.exists():
        return False

    return True


def check_file_system_file(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper refers to a file.

    Args:
        callable_wrapper:
            The callable wrapper to get checked.

    Returns:
        Whether the checked callable wrapper refers to a file.
    """

    file_system_path = callable_wrapper.parent_imported_callable()

    if not file_system_path:
        return False

    return file_system_path.is_file()


def check_file_system_directory(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper refers to a directory.

    Args:
        callable_wrapper:
            The callable wrapper to get checked.

    Returns:
        Whether the checked callable wrapper refers to a directory.
    """

    file_system_path = callable_wrapper.parent_imported_callable()

    if not file_system_path:
        return False

    return file_system_path.is_dir()


def check_file_system_module(
        callable_wrapper: CallableWrapper
) -> bool:
    """Checks whether the callable wrapper refers to a python file module.

    Args:
        callable_wrapper:
            The callable wrapper to get checked.

    Returns:
        Whether the checked callable wrapper refers to a python file module.
    """

    file_path: pathlib.Path = callable_wrapper.parent_imported_callable()

    return file_path.suffix == PYTHON_FILE_SUFFIX


def import_file_system_path(
        callable_wrapper: CallableWrapper
) -> pathlib.Path:
    """Imports the callable wrapper's file system path.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The file system path of the callable wrapper.
    """

    path = pathlib.Path(
        callable_wrapper.import_statement[0]
    )

    resolved_path = path.resolve()

    # TODO: Is Path restriction needed?
    if pathlib.Path.cwd() in resolved_path.parents:
        return path


def import_file_system_module(
        callable_wrapper: CallableWrapper
) -> types.ModuleType:
    """Imports the callable wrapper's file system Python module.

    Args:
        callable_wrapper:
            The callable wrapper to get imported.

    Returns:
        The imported Python module.
    """

    module_path: pathlib.Path = callable_wrapper.parent_imported_callable()

    module_spec = importlib.util.spec_from_file_location(
        name=module_path.stem,
        location=module_path
    )
    imported_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(imported_module)

    return imported_module

FILE_SYSTEM_HANDLER = CallableHandler(
    name="file_system",
    requires=None,
    check_function=check_file_system_path,
    import_function=import_file_system_path,
)
FILE_SYSTEM_FILE_HANDLER = CallableHandler(
    name="file_system_file",
    requires="file_system",
    check_function=check_file_system_file
)
FILE_SYSTEM_DIRECTORY_HANDLER = CallableHandler(
    name="file_system_directory",
    requires="file_system",
    check_function=check_file_system_directory
)
FILE_SYSTEM_MODULE_HANDLER = CallableHandler(
    name="file_system_module",
    requires="file_system_file",
    check_function=check_file_system_module,
    import_function=import_file_system_module
)


def get_callable_handler() -> List[CallableHandler]:
    """Returns the file system related callable handler instances."""

    return [
        FILE_SYSTEM_HANDLER,
        FILE_SYSTEM_FILE_HANDLER,
        FILE_SYSTEM_DIRECTORY_HANDLER,
        FILE_SYSTEM_MODULE_HANDLER
    ]
