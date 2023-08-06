"""
Plugin for automatic custom error handling.
"""
from enum import EnumMeta

from .exceptions import NoErrorHandlerFound


class ErrorLibrary:
    """These should be called automatically inside RPALibrary.

    1. Define error message texts  <-- robot code
    2. Raise exceptions with these texts  <-- robot code
    3. Detect these errors in to["last_error"]  <-- RPALibrary
    4. Handle the errors as defined in error handler methods  <-- RPALibrary

    Usage:

    .. code-block:: python

        from error_library import ErrorLibrary
        from error_handlers import ErrorHandlers  # write these yourself
        from errors import Errors  # write these yourself

        error_library = ErrorLibrary()
        error_library.handlers = ErrorHandlers
        error_library.errors = Errors

    Usage when using RPALibrary:

    First define ``Errors`` enum (in e.g. ``errors.py``) which contains
    descriptive error names and error messages as values. Ideally the error
    messages are so descriptive that they can be sent with error emails to
    business people.

    .. code-block:: python

        from enum import Enum

        class Errors(Enum):
            CANNOT_DIVIDE_BY_ZERO = "Cannot divide by zero"


    Then define ``ErrorHandlers`` class (in e.g. ``error_handlers.py``)
    which contains custom handlers for the known errors.

    .. code-block:: python

        from errors import Errors

        class ErrorHandlers:
            @error_name(Errors.CANNOT_DIVIDE_BY_ZERO)
            def handle_divide_by_zero(self, message):
                return message


    Then plug in your error handlers in your stage definition.
    Assign the imported classes in the constructor
    (e.g. ``self.errors.handlers = ErrorHandlers``). They are called
    automatically inside RPALibrary in the ``_predefined_action_on_fail``
    method.


    .. code-block:: python

        from TOSLibrary.RPALibrary import RPALibrary

        from error_handlers import ErrorHandlers
        from errors import Errors

        class Stage1(RPALibrary):

            def __init__(self):
                super(Stage1, self).__init__(*args)
                self.errors.handlers = ErrorHandlers
                self.errors.errors = Errors

            def main_action(self, to):
                raise ValueError(Errors.CANNOT_DIVIDE_BY_ZERO)

    """
    def __init__(self):
        self._handlers = None
        self._errors = None
        self.handler_names = tuple()

    @property
    def handlers(self):
        """External error handlers."""
        return self._handlers

    @handlers.setter
    def handlers(self, handlers):
        if not isinstance(handlers, type):
            raise TypeError("Handlers object should be a class")
        self._handlers = handlers()  # instantiate the class
        self.handler_names = tuple(self._get_handler_names())

    @property
    def errors(self):
        """External enum of error types."""
        return self._errors

    @errors.setter
    def errors(self, errors):
        if not isinstance(errors, EnumMeta):
            raise TypeError("Errors object should be an Enum")
        self._errors = errors

    def _get_handler_names(self):
        return filter(
            lambda a: not a.startswith('_') and callable(getattr(self.handlers, a)),
            dir(self.handlers)
        )

    def _get_handler_by_name(self, error_name):
        for name in self.handler_names:
            handler = getattr(self.handlers, name)
            if handler.name == error_name:
                return handler
        else:  # pylint: disable=W0120
            raise ValueError(f"No handler found for {error_name}")

    def find_error_type(self, to):
        if not to.get("last_error"):
            raise ValueError("Argument to should be a task object with 'last_error'")

        last_error = to["last_error"]
        error = tuple(filter(lambda err: err.value in last_error, self.errors))
        if not error or len(error) > 1:
            raise NoErrorHandlerFound(f"Unknown error: {last_error}")  # <-- what to do?
        return error[0]

    def get_error_handler(self, to):
        if not self._handlers and not self._errors:
            raise NoErrorHandlerFound("No handlers nor errors registered")
        error = self.find_error_type(to)
        handler = self._get_handler_by_name(error.name)
        return handler
