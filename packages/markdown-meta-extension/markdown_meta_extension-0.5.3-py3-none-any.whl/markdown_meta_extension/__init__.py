"""Importing Module.

This module provided the extensions for Python-Markdown (markdown).

Author:
    Martin Schorfmann
Since:
    2019-12-11
Version:
    2020-03-10
"""

from pathlib import Path
import re
import string
from typing import Any, Dict, List, Text, Tuple, Union
import xml.etree.ElementTree as etree

import click
from markdown import Markdown
from markdown.extensions import Extension
from markdown.util import Registry
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import Pattern, InlineProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor
from markupsafe import Markup
import yaml

try:
    from pelican.readers import MarkdownReader
    from pelican.utils import pelican_open
    PELICAN = True
except ImportError:
    PELICAN = False

from markdown_meta_extension.importing import Importer, CallableWrapper


FRONTMATTER_BLOCK_PRIORITY = 210
CALL_BLOCK_PRIORITY = 200
INLINE_CALL_PRIORITY = 200
TEMPLATE_PRIORITY = 0

SYNTAX_DEFAULTS = {
    "block_start": r"{{",
    "block_end": r"}}",
    "force_display_flag": "!",
    "assignment_operator": "=",
    "attribute_operator": ".",
    "block_surrounding_tag": "div",
    "inline_surrounding_tag": "span",
    "inline_call_pattern_regex": r"(\{\{)([\s\S]+?)(\}\})"
}

class MetaExtension(Extension):
    """Meta Extension for use in Python-Markdown."""

    def extendMarkdown(self, md: Markdown):  # pylint: disable=invalid-name
        """Extension method for registering extension parts.

        Extension method for registering the additional block processors.
        Furthermore a dictionary for meta data gets initialized.

        Args:
            md:
                Markdown parser object of Python-Markdown the extensions
                get registered on.
        """

        parser_registry: Registry = md.parser.blockprocessors

        # TODO: Initialize elsewhere
        md.meta_data = dict()
        md.meta_data["variables"] = dict()
        md.meta_data["statistics"] = dict()

        # TODO: Insert Syntax Defaults

        parser_registry.register(
            FrontmatterBlockProcessor(md.parser),
            "meta-frontmatter",
            FRONTMATTER_BLOCK_PRIORITY
        )

        call_processor = CallProcessor(md.meta_data, **SYNTAX_DEFAULTS)  # TODO: Replace with kwargs

        parser_registry.register(
            CallBlockProcessor(md.parser, call_processor),
            "meta-call",
            CALL_BLOCK_PRIORITY
        )

        inline_patterns_registry: Registry = md.inlinePatterns

        inline_call_pattern_regex = self.getConfig(
            "inline_call_pattern_regex",
            SYNTAX_DEFAULTS["inline_call_pattern_regex"]
        )

        inline_patterns_registry.register(
            CallInlineProcessor(
                inline_call_pattern_regex,
                call_processor,
                md=md
            ),
            "meta-inline-call",
            INLINE_CALL_PRIORITY
        )

        post_processor_registry: Registry = md.postprocessors

        post_processor_registry.register(
            TemplatePostProcessor(md),
            "meta-template",
            TEMPLATE_PRIORITY
        )


class MetaExtensionBlockProcessor(BlockProcessor):
    """Abstract super class for Meta Extension block processors.

    Offers several common convenience methods and properties.

    Attributes:
        meta_data:
            Meta Extension data of the parser
        has_frontmatter:
            Whether the document has a frontmatter
        imports:
            Access to the Importer of meta_data.
        variables:
            Access to the variables dict of meta_data.
    """

    def get_meta_data(self) -> Dict[Text, Any]:
        """Returns the parsers meta data dict."""
        return self.parser.md.meta_data

    meta_data = property(get_meta_data)

    def get_has_frontmatter(self) -> bool:
        """Returns the has-frontmatter flag from the meta data."""
        return bool(self.meta_data.get("has-frontmatter"))

    def set_has_frontmatter(self, value: bool = True):
        """Sets the has-frontmatter flag within the meta data."""
        self.meta_data["has-frontmatter"] = value

    has_frontmatter = property(
        get_has_frontmatter,
        set_has_frontmatter
    )

    def get_imports(self) -> Importer:
        """Returns the Importer instance from the meta data."""
        return self.meta_data.get("imports")

    def set_imports(self, value: Importer):
        """Sets the Importer instance within the meta data."""
        if not isinstance(value, Importer):
            raise ValueError(Importer)

        self.meta_data["imports"] = value

    imports = property(
        get_imports,
        set_imports
    )

    def get_variables(self) -> Dict[Text, Any]:
        """Returns the variables dict from the meta data."""
        return self.meta_data.get("variables")

    def set_variables(self, value: Dict[Text, Any]):
        """Sets the variables dict within the meta data."""
        if not isinstance(value, dict):
            raise ValueError(dict)

        self.meta_data["variables"] = value

    variables = property(
        get_variables,
        set_variables
    )

    def join_lines(self, lines: List[Text]) -> Text:
        """Joins the provided lines using linebreaks and returns the string."""
        # pylint: disable=no-self-use
        return "\n".join(lines)

class FrontmatterBlockProcessor(MetaExtensionBlockProcessor):
    """Block processor for parsing frontmatter blocks.

    Attributes:
        frontmatter_delimiter_pattern:
            Regular expression to detect frontmatter block delimiters.
        has_frontmatter:
            Whether the processed document already detected a frontmatter.
    """

    frontmatter_delimiter_pattern = re.compile(r"^-{3,}\s*$")

    # TODO: Where to reset flags when processing multiple documents?

    def does_line_contain_delimiter(self, line: Text) -> bool:
        """Whether the provided line contains a frontmatter delimiter."""
        return bool(self.frontmatter_delimiter_pattern.match(line))

    def is_block_delimited(self, block: Union[Text, List[Text]]) -> bool:
        """Whether the provided text block is delimited like a frontmatter."""
        if isinstance(block, str):
            block_lines = block.splitlines()
        else:
            block_lines = block

        if len(block_lines) < 2:
            return False

        first_block_line, *_, last_block_line = block_lines

        return (
            self.does_line_contain_delimiter(first_block_line)
            and self.does_line_contain_delimiter(last_block_line)
        )

    def is_block_frontmatter(self, block: Text) -> bool:
        """Whether the provided text block is a frontmatter block."""
        block_lines = block.splitlines()

        if not block_lines:
            return False

        has_delimiters = self.is_block_delimited(block_lines)

        return has_delimiters

    def test(self, parent: etree.Element, block: Text) -> bool:
        """Tests a text block whether it is a frontmatter.

        Only the first block displaying the characteristics of frontmatters
        is considered. All following fitting blocks will return False.

        Args:
            parent:
                The parent tree node of the text block.
            block:
                The text block which gets tested.

        Returns:
            Whether the text block is a frontmatter.
        """

        if self.has_frontmatter:
            return False

        is_frontmatter = self.is_block_frontmatter(block)

        if is_frontmatter:
            self.has_frontmatter = True

        return is_frontmatter

    def run(self, parent: etree.Element, blocks: List[Text]):
        """Parses and removes the frontmatter.

        Method for parsing and removing the frontmatter, when a frontmatter
        has been found. The parsed frontmatter is used for creating an Importer
        instance, which gets attached to the parser's meta data.

        Args:
            parent:
                The parent tree node of the affected blocks.
            blocks:
                A list of text blocks to get processed.
        """

        if self.has_frontmatter:
            frontmatter_block: Text = blocks.pop(0)

            _first_line, *content_lines, _last_line = frontmatter_block.splitlines()
            frontmatter_text: Text = self.join_lines(content_lines)

            self.imports = Importer(frontmatter_text)


class CallProcessor:
    """Helper class for processing block and inline calls."""

    def __init__(self, meta_data: Dict[Text, Any], **kwargs):

        self.meta_data = meta_data

        syntax_attributes: Dict[Text, Text] = SYNTAX_DEFAULTS
        syntax_attributes.update(kwargs)

        self.block_start = syntax_attributes.get("block_start")
        self.block_end = syntax_attributes.get("block_end")

        self.force_display_flag = syntax_attributes.get("force_display_flag")
        self.assignment_operator = syntax_attributes.get("assignment_operator")
        self.attribute_operator = syntax_attributes.get("attribute_operator")

        self.block_surrounding_tag = syntax_attributes.get("block_surrounding_tag")
        self.inline_surrounding_tag = syntax_attributes.get("inline_surrounding_tag")

    def get_imports(self) -> Importer:
        """Returns the Importer instance from the meta data."""
        return self.meta_data.get("imports")

    def set_imports(self, value: Importer):
        """Sets the Importer instance within the meta data."""
        if not isinstance(value, Importer):
            raise ValueError(Importer)

        self.meta_data["imports"] = value

    imports = property(
        get_imports,
        set_imports
    )

    def get_variables(self) -> Dict[Text, Any]:
        """Returns the variables dict from the meta data."""
        return self.meta_data.get("variables")

    def set_variables(self, value: Dict[Text, Any]):
        """Sets the variables dict within the meta data."""
        if not isinstance(value, dict):
            raise ValueError(dict)

        self.meta_data["variables"] = value

    variables = property(
        get_variables,
        set_variables
    )

    def remove_block_delimiters(self, block: Text) -> Text:
        """Returns the provided block without its delimiters."""
        block = block.strip()
        return block[len(self.block_start):-len(self.block_end)]

    def has_line_force_display_flag(self, line: Text) -> bool:
        """Whether the provided line starts with a force display flag."""
        return line.startswith(self.force_display_flag)

    def remove_line_force_display_flag(self, line: Text) -> Text:
        """Returns the line without force display flag and outer whitespace."""
        _line_start, remaining_line = line.split(self.force_display_flag)

        return remaining_line.strip()

    def is_line_assignment(self, line: Text) -> bool:
        """Whether the provided line represents an assignment."""
        return self.assignment_operator in line

    def process_call(self, line: Text) -> Tuple[Text, Text]:
        """Processes a call without an assignment.

        Args:
            line:
                The line or line part to get processed

        Returns:
            A tuple consisting of the call expression part
            and the remaining line part.
            The remaining line part can be None.
        """
        # pylint: disable=no-self-use

        line = line.strip()

        if any(
                whitespace_character in line
                for whitespace_character in string.whitespace
        ):
            call_expression, remaining = line.split(maxsplit=1)
        else:
            call_expression = line
            remaining = None

        return call_expression, remaining

    def process_assignment(self, line: Text) -> Tuple[Text, Text, Text]:
        """Processes a call with an assignment.

        Args:
            line:
                The line to get processed.

        Returns:
            A tuple consisting of the parts
            variable name, call expression and what remains of the line.
            The remaining part may be None.
        """
        variable_name, remaining = line.split(
            self.assignment_operator
        )
        variable_name: Text = variable_name.strip()
        remaining: Text = remaining.strip()

        call_expression, remaining = self.process_call(remaining)

        return variable_name, call_expression, remaining

    def has_call_expression_attribute(self, call_expression: Text) -> bool:
        """Whether the provided call expression has an attribute access."""
        return self.attribute_operator in call_expression

    def join_lines(self, lines: List[Text]) -> Text:
        """Joins the provided lines using linebreaks and returns the string."""
        # pylint: disable=no-self-use
        return "\n".join(lines)

    def process_arguments(self, arguments: Union[List, Dict]) -> Union[List, Dict]:

        if isinstance(arguments, list):
            processed_arguments = [
                self.run(argument, allow_display=False) if isinstance(argument, str) and (
                    argument.startswith(self.block_start)
                    and argument.endswith(self.block_end)
                ) else argument
                for argument in arguments
            ]

        elif isinstance(arguments, dict):
            processed_arguments = {
                key: self.run(argument, allow_display=False) if isinstance(argument, str) and (
                    argument.startswith(self.block_start)
                    and argument.endswith(self.block_end)
                ) else argument
                for key, argument in arguments.items()
            }
        else:
            processed_arguments = arguments

        return processed_arguments

    def create_markup(
            self,
            markup: Any,
            is_inline: bool,
            surround: Text = None
    ) -> etree.Element:
        if markup is None:
            return None

        if hasattr(markup, "__html__"):
            markup = markup.__html__()

        try:
            markup_node = etree.fromstring(str(markup))

            if surround:
                surrounding_node = etree.Element(surround)
                surrounding_node.append(markup_node)
                markup_node = surrounding_node
        except etree.ParseError:

            if isinstance(markup, list):

                if is_inline:
                    inline_list = etree.Element(self.inline_surrounding_tag)
                    inline_list.text = ""

                    markup_list = [
                        self.create_markup(list_item, is_inline)
                        for list_item
                        in markup
                    ]

                    for index, markup_item in enumerate(markup_list):
                        if index + 1 < len(markup_list):
                            markup_item.tail = ", "

                        inline_list.append(markup_item)

                    markup_node = inline_list
                else:
                    unordered_list = etree.Element("ul")

                    for list_item in markup:
                        list_item_markup = self.create_markup(
                            list_item,
                            is_inline,
                            surround="li"
                        )
                        unordered_list.append(
                            list_item_markup
                        )

                    markup_node = unordered_list

            elif isinstance(markup, dict):
                definition_list = etree.Element("dl")

                for term, description in markup.items():
                    term_markup = self.create_markup(
                        term,
                        is_inline,
                        surround="dt"
                    )
                    description_markup = self.create_markup(
                        description,
                        is_inline,
                        surround="dd"
                    )

                    definition_list.append(
                        term_markup
                    )
                    definition_list.append(
                        description_markup
                    )

                markup_node = definition_list
            else:
                if surround:
                    surrounding_tag = surround
                else:
                    surrounding_tag = self.inline_surrounding_tag\
                        if is_inline\
                        else self.block_surrounding_tag

                markup_node = etree.Element(
                    surrounding_tag
                )
                try:
                    markup_node_child = etree.fromstring(str(markup))

                    if surround:
                        markup_node.append(markup_node_child)
                    else:
                        markup_node = markup_node_child
                except (etree.ParseError, TypeError):
                    markup_node.text = str(markup)

        return markup_node

    def run(self, block: Text, allow_display: bool = True) -> etree.Element:
        """Method which processes detected call block.

        Method which processes detected call block and returns their result.

        Args:
            block:
                The text block which gets processed.
        """
        self.meta_data["statistics"]["calls"] =\
            self.meta_data["statistics"].get("calls", 0) + 1

        # Block processing and separation
        block = self.remove_block_delimiters(block)

        try:
            variables_assignment = yaml.safe_load(block)
            if isinstance(variables_assignment, dict):
                processed_variables_assignment = self.process_arguments(
                    variables_assignment
                )
                self.variables.update(processed_variables_assignment)
                return None
            else:
                pass

        except yaml.YAMLError:
            pass

        block_lines = block.splitlines()
        first_line, *remaining_lines = block_lines

        # Force display flag detection and removal
        force_display = self.has_line_force_display_flag(first_line)

        if force_display:
            first_line = self.remove_line_force_display_flag(first_line)

        # Assignment detection and processing
        is_assignment = self.is_line_assignment(first_line)

        if is_assignment:
            # Call with assignment
            variable_name, call_expression, remaining = self.process_assignment(
                first_line
            )

            display = force_display
        else:
            # Call without assignment
            variable_name = None
            call_expression, remaining = self.process_call(first_line)
            display = True

        # Attribute access detection and processing
        has_attribute = self.has_call_expression_attribute(call_expression)

        if has_attribute:
            call_expression, *call_names = call_expression.split(
                self.attribute_operator
            )
        else:
            variable = None
            call_names = None

        # Variable or imported callable retrieval
        variable = self.variables.get(call_expression)

        if not variable:
            variable = self.imports.get(call_expression)

        callable_variable = variable

        # Optional Access of attributes to replace callable variable
        if call_names:
            for call_name in call_names:
                try:
                    callable_variable = callable_variable[call_name]
                except (KeyError, TypeError):
                    if hasattr(callable_variable, call_name):
                        callable_variable = getattr(callable_variable, call_name)
                    else:
                        try:
                            callable_variable = callable_variable[int(call_name)]
                        except ValueError:
                            callable_variable = KeyError(
                                f"Cannot find name '{call_name}' in variable."
                            )


        # Arguments parsing
        if not remaining:
            remaining = self.join_lines(remaining_lines)

        arguments = yaml.safe_load(
            remaining
        )

        arguments = self.process_arguments(arguments)

        # Abort in case of still no callable variable
        if callable_variable is None:  # FIXME: What to do?
            return None

        # Supplying the arguments to the call of the callable
        if isinstance(callable_variable, CallableWrapper):
            callable_result = callable_variable(arguments)
        else:
            if arguments:
                if isinstance(arguments, dict):
                    callable_result = callable_variable(**arguments)
                elif isinstance(arguments, list):
                    callable_result = callable_variable(*arguments)
                else:
                    callable_result = callable_variable(arguments)
            else:
                try:
                    callable_result = callable_variable()
                except TypeError:
                    callable_result = callable_variable

        # Assigning the call result in case of an assignment
        if is_assignment and variable_name:
            self.variables[variable_name] = callable_result

        # Returning the result markup node
        if allow_display and display:
            markup_output = callable_result

            is_inline = (len(remaining_lines) < 1)

            markup_node = self.create_markup(
                markup_output,
                is_inline
            )

            return markup_node
        elif not allow_display:
            return callable_result

        return None

    def __call__(self, block: Text) -> etree.Element:
        return self.run(block)


class CallBlockProcessor(MetaExtensionBlockProcessor):
    """Block processor for processing call blocks.

    Block processor which processes detected call blocks.
    Call blocks are used to invoke functions or constructor calls.

    Attributes:
        block_start:
            Regular expression of the start indicator of a call block.
        block_end:
            Regular expression of the end indicator of a call block.
        force_display_flag:
            The character used as a flag for forcing the display of the call's
            results.
        assignment_operator:
            The character used as an operator for assigning results to a
            variable.
        attribute_operator:
            The character used to access attributes or methods of an object
            variable.
    """

    def __init__(self, parser, call_processor: CallProcessor):
        super().__init__(parser)

        self.call_processor = call_processor

    def test(self, parent: etree.Element, block: Text) -> bool:
        """Method for testing a text block, whether it is a call block.

        Args:
            parent:
                The parent tree node of the text block.
            block:
                The text block to get tested, whether it is a call block.

        Returns:
            Whether the text block is a call block.
        """

        block = block.strip()

        return (
            block.startswith(self.call_processor.block_start)
            and block.endswith(self.call_processor.block_end)
        )

    def run(self, parent: etree.Element, blocks: List[Text]):
        """Method which processes detected call blocks.

        Method which processes detected call blocks and attaches their results
        to the parent tree node.

        Args:
            parent:
                The parent tree node.
            blocks:
                The list of text blocks which gets processed.
        """

        block: Text = blocks.pop(0)

        markup_node = self.call_processor(block)

        if markup_node is not None:
            parent.append(
                markup_node
            )


class CallInlineProcessor(InlineProcessor):
    """Processor for inline calls.

    Attributes:
        call_processor:
            The processor for handling calls.
    """

    def __init__(
            self,
            pattern,
            call_processor: CallProcessor,
            md: Markdown = None
    ):
        """Initializes the inline call processor."""
        super().__init__(pattern, md=md)

        self.call_processor = call_processor

    def handleMatch(self, m, data: Text) -> Tuple[etree.Element, int, int]:
        markup_node: etree.Element = self.call_processor(
            data[m.start(0):m.end(0)]
        )
        return markup_node, m.start(0), m.end(0)


class TemplatePostProcessor(Postprocessor):

    def run(self, text: Text) -> Text:
        """Wraps the existing markup tree in a template with meta data."""

        data = self.md.meta_data
        importer = data.get("imports", Importer(dict()))
        template = importer.template
        meta_data = importer.meta_data

        if template is not None:
            self.md.stripTopLevelTags = False
            meta_data["content"] = Markup(
                text
            )
            result = template(meta_data)

            return result

        return text


def makeExtension(**kwargs):  # pylint: disable=invalid-name
    """Function returning an instance of the extension."""

    return MetaExtension(**kwargs)


def get_parser() -> Markdown:
    """Returns a Markdown parser including the Markdown Meta Extension."""
    return Markdown(
        extensions=[
            MetaExtension()
        ]
    )


def convert(input_path: Text, output_path: Text = None):
    """Converts an input Markdown file to an output HTML file.

    Args:
        input_path:
            The path to the input Markdown file.
        output_path:
            Optional path for the HTML output.
            If not provided, path is based on input path.
    """
    parser = get_parser()
    input_path = Path(input_path)

    if not output_path:
        output_path = input_path.with_suffix(".html")
    else:
        output_path = Path(output_path)

    output_path.write_text(
        parser.convert(input_path.read_text())
    )


def convert_from_string(input_string: Text) -> Text:
    parser = get_parser()
    return parser.convert(input_string)


@click.command()
@click.argument(
    "input_path",
    required=True,
    type=click.Path(writable=True)
)
@click.option(
    "output_path",
    "--output",
    "-o",
    required=False,
    default=None,
    type=click.Path(),
    help="The optional path for the HTML output."
)
@click.option(
    "quiet",
    "--quiet",
    "-q",
    is_flag=True,
    flag_value=True,
    help="Mute all command line output."
)
@click.option(
    "verbose",
    "--verbose",
    "-v",
    is_flag=True,
    flag_value=True,
    help="Display additional command line output and file contents."
)
@click.option(
    "yes",
    "--yes",
    "-y",
    is_flag=True,
    flag_value=True,
    help="Confirm overwriting existing output file."
)
def markdown_meta_extension_parser(
        input_path: Text,
        output_path: Text = None,
        quiet: bool = False,
        verbose: bool = False,
        yes: bool = False
):
    """CLI command for converting an input Markdown file to an output HTML file.

    Args:
        input_path:
            The path to the Markdown file to get processed.
        output_path:
            The optional path for the output HTML file.
            If not provided, it is based on the input path.
        quiet:
            Flag for muting console output for this command.
        verbose:
            Flag whether to display additional information during conversion.
        yes:
            Flag whether to skip overwrite confirmation dialog with yes.
    """
    input_path = Path(input_path)

    if verbose and not quiet and input_path.suffix not in [".md", ".markdown"]:
        click.echo(f"Input file {input_path} has an unexpected extension.")

    if not output_path:
        output_path = input_path.with_suffix(".html")
        if not quiet:
            click.echo(f"Output path {output_path} is assumed.")
    else:
        output_path = Path(output_path)

    parser = get_parser()

    if verbose and not quiet:
        click.echo(
            "Markdown parser with Markdown Meta Extension "
            "successfully initialized."
        )

    input_string = input_path.read_text()

    if verbose and not quiet:
        click.echo()
        click.echo(input_string)

    output_string = parser.convert(input_path.read_text())

    if not quiet:
        # pylint: disable=no-member
        number_imports = len(parser.meta_data.get("imports", dict()))
        click.echo(f"{number_imports} callables were imported.")

        number_calls = parser.meta_data["statistics"].get("calls", 0)
        click.echo(f"{number_calls} calls were made.")

    if verbose and not quiet:
        click.echo()
        click.echo(output_string)

    write_file = True
    if output_path.exists():
        write_file = (
            yes or
            click.confirm(f"Confirm overwriting output file {output_path}.")
        )
        if write_file:
            if not quiet:
                click.echo(f"File {output_path} will be overwritten.")
        else:
            if not quiet:
                click.echo(f"Aborted writing to file {output_path}.")

    if write_file:
        output_path.write_text(output_string)
        if not quiet:
            click.echo(f"Output written to file {output_path}.")

@click.command()
@click.argument(
    "glob",
    required=True,
    type=click.STRING
)
@click.option(
    "directory",
    "--directory",
    "-d",
    required=False,
    default=None,
    type=click.Path(dir_okay=True, exists=True),
    help="The optional directory for the glob pattern."
)
def markdown_meta_extension_glob_parser(
        glob,
        directory
):
    """Parses files corresponding to glob pattern in directory.

    Args:
        glob:
            The glob pattern to match the files to get parsed.
        directory:
            The optional starting point for the glob pattern.
            Defaults to current working directory.
    """
    if not directory:
        directory = Path.cwd()
    else:
        directory = Path(directory)

    input_file_paths = list(directory.glob(glob))

    with click.progressbar(input_file_paths) as progress_bar:
        for input_file_path in progress_bar:
            convert(
                input_file_path
            )


if PELICAN:

    class MarkdownMetaExtensionPelicanReader(MarkdownReader):
        """Reader for Markdown Meta Extension files."""

        enabled = bool(MetaExtension)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            settings = self.settings["MARKDOWN"]

            if "markdown_meta_extension" not in settings["extensions"]:
                settings["extensions"].append("markdown_meta_extension")

            settings["extensions"].pop("markdown.extensions.meta")

        def _parse_metadata(self, meta):
            """Return the dict containing document metadata"""

            return NotImplementedError

        def read(self, source_path):
            """Parse content and metadata of markdown files"""

            self._source_path = source_path
            self._md = Markdown(**self.settings["MARKDOWN"])
            with pelican_open(source_path) as text:
                content = self._md.convert(text)

            if hasattr(self._md, "meta_data"):
                # pylint: disable=no-member
                metadata = self._md.meta_data.get("meta-data", dict())
            else:
                metadata = dict()

            return content, metadata
