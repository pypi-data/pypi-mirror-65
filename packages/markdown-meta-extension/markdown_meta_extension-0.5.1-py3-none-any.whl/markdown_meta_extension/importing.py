"""Importing Module.

This Module provides the Importer class, which is used for processing
the imports frontmatter of a document.

Author:
    Martin Schorfmann
Since:
    2019-12-14
Version:
    2020-02-27
"""

import collections
from pathlib import Path
from typing import Any, Callable, Dict, List, Text, Union

import yaml

from .plugins.spec import CallableWrapper


INTER_PATH_SEPARATOR = ":"  # TODO: Import instead of hardcoding


class Importer(collections.UserDict):  # pylint: disable=too-many-ancestors
    """Imports callables according to frontmatter dict.

    Imports callables according to the frontmatter dict upon instantiation.

    Attributes:
        source:
            The source dictionary containing textual or list import statements
            mapped to keys
        data:
            Internal dictionary mapping from a key to a callable wrapper
            for each key.
    """

    source: Dict[Text, Text]
    data: Dict[Text, CallableWrapper]
    meta_data: Dict[Text, Any]

    def __init__(
            self,
            source: Union[Text, Dict[Text, Union[Text, List[Text]]]]
    ):
        """Initializes Importer with the import frontmatter.

        Processes the import frontmatter and referenced external import files
        into a single dictionary for accessing the callable wrappers by key.

        Args:
            source:
                The mapping from key to import statements in form of a dict or
                a parsable YAML source string.
        """

        if isinstance(source, str):
            source = yaml.safe_load(source)

        meta_data = source.pop("meta-data", dict())

        predefined_source = self.process_predefined(
            source.pop("import", list())
        )

        predefined_source.update(source)

        self.source = predefined_source

        super().__init__(
            self.process_source(
                self.source
            )
        )

        predefined_meta_data = self.process_predefined(
            source.pop("meta-data-import", list())
        )

        predefined_meta_data.update(meta_data)

        template = predefined_meta_data.pop("template", None)

        if template:
            if not isinstance(template, list):
                template = template.split(INTER_PATH_SEPARATOR)

            self.template = CallableWrapper.import_callable(
                import_key="template",
                import_statement=template
            )
        else:
            self.template = None

        self.meta_data = predefined_meta_data

    @classmethod
    def process_source(
            cls,
            source: Dict[Text, Union[Text, List[Text]]]
    ) -> Dict[Text, Callable]:
        """Processes the source import statements.

        Args:
            source:
                The source mapping from key to import statement
                (Either string with separator chars or list).

        Returns:
            The processed imports containing callable wrappers as values.
        """

        processed_source = dict()

        for key, callable_path in source.items():

            if not isinstance(callable_path, list):
                callable_path = callable_path.split(INTER_PATH_SEPARATOR)

            processed_source[key] = CallableWrapper.import_callable(
                import_key=key,
                import_statement=callable_path,
                plugin_name=None  # TODO: Pass plugin name
            )

        return processed_source

    @classmethod
    def process_predefined(
            cls,
            predefined: List[Text]
    ) -> Dict[Text, Text]:
        """Processes external import YAML files.

        Reads in and merges predefined import YAML files.

        Args:
            predefined:
                List of file paths.

        Returns:
            Mapping from keys to import statements, where
            earlier non-unique keys got overridden by later keys of the same
            key value.
        """

        predefined_source = dict()

        for predefined_item in predefined:
            predefined_item_path = Path(predefined_item)

            predefined_source.update(
                yaml.safe_load(predefined_item_path.read_text())
            )

        return predefined_source
