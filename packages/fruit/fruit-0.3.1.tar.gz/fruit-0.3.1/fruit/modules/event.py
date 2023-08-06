"""
Event module for implementing event based programming in Python.
"""

from typing import Callable, List
from inspect import signature


class Event(object):
    """Event class for event based programming in python.

    To add event handlers to a created event either use `Event.subscribe()` or
    the += operator.

    Example::
        my_event = Event()
        my_event.subscribe(new_handler)
        my_event += new_handler
    """

    __handlers : List[Callable[[any], any]] = None
    __args = None
    __kwargs = None

    def __init__(self, *args, **kwargs):
        self.__handlers = list()

        # Store a call signature to the object
        self.__args = args
        self.__kwargs = kwargs

    def __verify_signature(self, event_handler: Callable[[any], any]):
        """
        Try to bind the given example call of the event handler to the `event_handler`.
        In case of a signature mismatch, TypeError will be raised.

        Parameters
        ----------
        `event_handler` : Callable[[any], any]
            Event handler to verify.
        Raises
        ------
        TypeError:
            Invalid event_handler signature
        """
        try:
            signature(event_handler).bind(*self.__args, **self.__kwargs).apply_defaults()
        except TypeError as te:
            # Add a diagnostic message to the TypeError
            error = f"""The signature of '{event_handler.__name__}' is invalid for this event.
            Reason: {str(te)}"""
            raise TypeError(error)


    def subscribe(self, event_handler: Callable[[any], any]) -> None:
        """
        Subscribe to the event. When the event is triggered, the passed
        event handler will be called with the passed arguments.

        Parameters
        ----------
        `event_handler` : Callable[[any], any]
            Event handler to add
        Raises
        ------
        ValueError:
            The event handler is already subscribed to the event!
        """
        if callable(event_handler):
            if event_handler in self.__handlers:
                raise ValueError("The event handler is already subscribed to the event!")
            else:
                self.__verify_signature(event_handler)
                self.__handlers.append(event_handler)

    def unsubscribe(self, event_handler: Callable[[any], any], ignore_errors=True) -> None:
        """
        Unsubscribe from the event. Removes the given event handler function from the list
        of event handlers.

        Parameters
        ----------
        `event_handler` : Callable[[any], any]
            Event handler to remove
        ignore_errors : bool, optional
            If False a `ValueError` will be raise, when the event handler was not subscribed, by default True
        """
        try:
            self.__handlers.remove(event_handler)
        except ValueError:
            if not ignore_errors:
                raise

    def __iadd__(self, other: Callable[[any], any]):
        """
        Overload the += operator to call the `Event.subscribe()` function.

        Example::
            my_event += new_handler

        Parameters
        ----------
        `other` : Callable[[any], any]
            Event handler to add
        """
        self.subscribe(event_handler=other)
        return self

    def __isub__(self, other: Callable[[any], any]):
        """
        Overload the -= operator to call `Event.unsubscribe()`.

        Parameters
        ----------
        `other` : Callable[[any], any]
            Event handler to remove.
        """
        self.unsubscribe(event_handler=other)
        return self

    def __call__(self, *args, **kwargs):
        for each_handler in self.__handlers:
            each_handler(*args, **kwargs)