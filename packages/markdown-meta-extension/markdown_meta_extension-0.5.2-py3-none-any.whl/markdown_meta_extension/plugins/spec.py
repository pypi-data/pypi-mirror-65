"""Callable Wrapper and Handler Specification.

This module specifies the wrapper around importable callables and the class
used by handler plugins.
Instances of the class provide functionality around the import and
use of certain callables according to import statements.

Author:
    Martin Schorfmann
Since:
    2020-01-26
Version:
    2020-02-27
"""

from typing import Any, Callable, Dict, List, Text, Union


class CallableWrapper:
    """Wrapper class around callables.

    Wrapper class around callables, which provides import, call and get
    functionality by using implemented instances of CallableHandler.

    Attributes:
        import_key:
            The key the callable wrapper or following callable wrappers
            will be accessible by.
        import_statement:
            The import statement list used by the callable handlers
            for importing the callable.
        plugin_name:
            An optional plugin name to give handling to the plugin of this name.
        callable_handler:
            The callable handler used to manage this callable.
        parent:
            The parent callable wrapper if this wrapper is not the first stage.
        imported_callable:
            The imported callable for use or the intermediate object for
            further importing.
    """

    import_key: Text
    import_statement: List[Text]
    plugin_name: Text
    callable_handler: "CallableHandler"
    parent: "CallableWrapper"
    imported_callable: Any

    @classmethod
    def import_callable(
            cls,
            import_key: Text,
            import_statement: List[Text],
            plugin_name: Text = None
    ) -> "CallableWrapper":
        """Imports the final callable.

        Imports the final callable through a sequence of intermediate callable
        wrappers.

        Args:
            import_key:
                The key the final callable wrapper will be accessible by.
            import_statement:
                The list of import statement parts used for the import.
            plugin_name:
                The optional name of the plugin to use for importing.

        Returns:
            The final callable wrapper of the import.
        """

        imported_callable_wrapper = None

        # pylint: disable=unused-variable
        while imported_callable_wrapper is None or (
                imported_callable_wrapper.callable_handler\
                and imported_callable_wrapper.callable_handler\
                    .has_following_handlers()
        ):
            # TODO: How to determine iterations?
            imported_callable_wrapper = CallableWrapper(
                import_key=import_key,
                import_statement=import_statement,
                plugin_name=plugin_name,
                parent=imported_callable_wrapper
            )

        if not imported_callable_wrapper.is_functional():
            return imported_callable_wrapper.parent

        return imported_callable_wrapper


    def __init__(
            self,
            import_key,
            import_statement: Text,
            plugin_name: Text = None,
            callable_handler=None,
            parent=None,
            imported_callable=None
    ):
        """Initializes a callable wrapper.

        Args:
            import_key:
                The key the callable wrapper or following callable wrappers
                will be accessible by.
            import_statement:
                The import statement list used by the callable handlers
                for importing the callable.
            plugin_name:
                An optional plugin name to give handling to the plugin of this name.
            callable_handler:
                An optional preselected callable handler.
            parent:
                The optional parent callable wrapper if this wrapper is not the first stage.
            imported_callable:
                Optionally the imported callable
        """

        self.import_key = import_key
        self.import_statement = import_statement
        self.plugin_name = plugin_name
        self.parent = parent
        self.imported_callable = imported_callable

        if not callable_handler:
            self.callable_handler = CallableHandler.assign_handler_type(
                self
            )
        else:
            self.callable_handler = callable_handler

        if self.callable_handler:
            self.imported_callable = self.callable_handler.import_callable(
                self
            )

    def parent_handler_name(self) -> Text:
        """Shortcut method for the name of the parent handler."""

        if self.parent and self.parent.callable_handler:
            return self.parent.callable_handler.name

        return None

    def parent_imported_callable(self) -> Any:
        """Shortcut method for the imported callable of the parent handler."""

        if self.parent and self.parent.imported_callable:
            return self.parent.imported_callable

        return None

    def is_functional(self) -> bool:
        """Whether the callable is functional."""

        return bool(self.callable_handler and self.imported_callable)

    def __bool__(self) -> bool:
        return self.is_functional()

    def __call__(self, arguments=None) -> Any:
        """Delegates call to callable handler and returns its result."""

        if self.is_functional():
            return self.callable_handler(self, arguments)
        else:
            try:
                return self.callable_handler(self, arguments)
            except TypeError:
                return self.imported_callable

    def __getitem__(self, key: Union[Text, List]) -> "CallableWrapper":
        """Delegates getting of an item to the handler returns item wrapper."""

        if self.is_functional():
            if isinstance(key, list):
                callable_wrapper = None

                for partial_key in key:
                    callable_wrapper = self.callable_handler.get_child(
                        self,
                        partial_key
                    )

            else:
                callable_wrapper = self.callable_handler.get_child(
                    self,
                    key
                )

            return callable_wrapper

        return None


class CallableHandler:
    """Handlers for handling importing and calling of callables.

    Attributes:
        all_handlers:
            Mapping from handler names to callable handler instances.
        initial_handlers:
            List of initally usable handlers.
        following_handlers:
            Mapping from handler keys to a lists of following handlers.
        name:
            Name of the handler instance.
        requires:
            Required handler names to come before this handler.
        check_function:
            Function used to check if this handler is applicable for
            a callable wrapper.
        import_function:
            Function used for proceeding with the callable import
            in this stage.
        call_function:
            Function used for defining call behavior of the callable wrapper.
        get_function:
            Function used for getting child elements of the callable wrapper.
    """

    all_handlers: Dict[Text, "CallableHandler"] = dict()
    initial_handlers: List["CallableHandler"] = list()
    following_handlers: Dict[Text, "CallableHandler"] = dict()

    def __init__(
            self,
            name: Text,
            requires: Union[Text, List[Text]],
            check_function: Callable[
                [CallableWrapper], bool
            ],
            import_function: Callable[
                [CallableWrapper], Any
            ] = None,
            call_function: Callable[
                [CallableWrapper, Union[List, Dict]], Any
            ] = None,
            get_function: Callable[
                [CallableWrapper, Text], CallableWrapper
            ] = None
    ):
        """Initializes a handler instance.

        Also registers this handler with its class.

        Args:
            name:
                Name of the handler instance.
            requires:
                Required handler names or single name to come
                before this handler.
            check_function:
                Function used to check if this handler is applicable for
                a callable wrapper.
            import_function:
                Function used for proceeding with the callable import
                in this stage.
            call_function:
                Function used for defining call behavior of
                the callable wrapper.
            get_function:
                Function used for getting child elements of
                the callable wrapper.
        """

        self.name = name
        self.requires = requires if isinstance(requires, list) else [requires]
        self.check_function = check_function
        self.import_function = import_function
        self.call_function = call_function
        self.get_function = get_function

        CallableHandler.register_handler(self)

    @classmethod
    def register_handler(
            cls,
            callable_handler: "CallableHandler"
    ):
        """Registers the handler instance with its class."""

        name = callable_handler.name
        cls.all_handlers[name] = callable_handler

        for requirement in callable_handler.requires:
            if requirement is None:
                cls.initial_handlers.append(callable_handler)
            else:
                if requirement not in cls.following_handlers:
                    cls.following_handlers[requirement] = list()

                cls.following_handlers[requirement].append(callable_handler)

    @classmethod
    def assign_handler_type(
            cls,
            callable_wrapper: CallableWrapper
    ) -> "CallableHandler":
        """Assigns the fitting handler instance to the callable wrapper"""
        if not callable_wrapper.parent:
            callable_handlers = cls.initial_handlers
        else:
            callable_handlers = cls.following_handlers.get(
                callable_wrapper.parent_handler_name(),
                list()
            )

        for callable_handler in callable_handlers:
            if callable_handler.check(
                    callable_wrapper=callable_wrapper
            ):
                return callable_handler

        return None

    def has_following_handlers(self) -> bool:
        """Whether this handler has following handlers."""

        return bool(
            self.following_handlers.get(self.name)
        )

    def check(
            self,
            callable_wrapper
    ) -> bool:
        """Wrapper function around check function."""

        return bool(self.check_function(callable_wrapper))

    def import_callable(
            self,
            callable_wrapper
    ) -> Any:
        """Imports callable using this handler or returns parent callable."""
        if self.import_function:
            imported_callable = self.import_function(
                callable_wrapper
            )
        elif callable_wrapper.parent:
            imported_callable = callable_wrapper.parent_imported_callable()
        else:
            imported_callable = None

        return imported_callable


    def __call__(
            self,
            callable_wrapper: CallableWrapper,
            arguments: Union[List[Any], Dict[Text, Any]]
    ) -> Any:
        """Handles calls for callable wrapper.

        Defines some default behavior if a custom call function is absent.

        Args:
            callable_wrapper:
                The callable wrapper whose callable will be called.
            arguments:
                Ordered arguments or keyworded arguments
                (Includes no arguments).

        Returns:
            The result of the call to the callable wrapper's callable.
        """

        if not self.call_function:
            try:
                if not arguments:
                    returned_result = callable_wrapper.imported_callable()
                elif isinstance(arguments, dict):
                    returned_result = callable_wrapper.imported_callable(
                        **arguments
                    )
                elif isinstance(arguments, list):
                    returned_result = callable_wrapper.imported_callable(
                        *arguments
                    )
                else:
                    raise TypeError(
                        "Type of call arguments '{arguments}' not considered.".format(
                            arguments=arguments
                        )
                    )
            except TypeError:  # TODO: Error handling
                returned_result = callable_wrapper.imported_callable
        else:
            returned_result = self.call_function(
                callable_wrapper=callable_wrapper,
                arguments=arguments
            )

        return returned_result

    def get_child(
            self,
            callable_wrapper: CallableWrapper,
            key: Text
    ) -> CallableWrapper:
        """Returns the child element of the callable wrapper.

        Defines some default behavior in case of absence of
        a custom get function.

        Args:
            callable_wrapper:
                The callable wrapper whose callable's child elements gets
                accessed.
            key:
                The key for accessing the child element.

        Returns:
            The accessed child element wrapped in a callable wrapper.
        """

        if not self.get_function:
            if hasattr(callable_wrapper.imported_callable, "__getitem__"):
                child_item = callable_wrapper.imported_callable[key]
            else:
                child_item = getattr(
                    callable_wrapper.imported_callable,
                    key
                )
        else:
            child_item = self.get_function(
                callable_wrapper=callable_wrapper,
                key=key
            )

        if not isinstance(child_item, CallableWrapper):
            child_item = CallableWrapper(
                import_key=callable_wrapper.import_key,
                import_statement=callable_wrapper.import_statement + [key],
                plugin_name=callable_wrapper.plugin_name,
                callable_handler=None,
                parent=callable_wrapper,
                imported_callable=child_item
            )

        return child_item
