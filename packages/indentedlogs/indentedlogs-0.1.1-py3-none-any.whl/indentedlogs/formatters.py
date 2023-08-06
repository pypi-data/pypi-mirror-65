import logging
from typing import Callable, Iterable, Optional, Type

from .monitor import Monitor, StackMonitor


class StackedFormatter(logging.Formatter):
    def __init__(self, parent_formatter: logging.Formatter,
                 child_formatter: logging.Formatter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent_formatter = parent_formatter
        self._child_formatter = child_formatter

    def format(self, record: logging.LogRecord) -> str:
        record.msg = self._child_formatter.format(record)
        return self._parent_formatter.format(record)


class IndentingFormatter(logging.Formatter):
    def __init__(self, monitor: Monitor, indentation: str,
                 deepest_indentation: str, max_level: Optional[int], *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._monitor = monitor
        self._indentation = indentation
        self._deepest_indentation = deepest_indentation
        self._max_level = max_level

    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        level = self._monitor.get_level()

        if self._max_level and level > self._max_level:
            return self._indentation * (
                self._max_level - 1) + self._deepest_indentation + message
        else:
            return self._indentation * level + message


class DefaultLogger:
    """Used just to improve rendering of API documentation."""
    value = (logging.Logger, )

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return '(logging.Logger,)'

    def __iter__(self):
        pass


def install(
    indentation: str = '  ',
    deepest_indentation: str = '..',
    max_level: Optional[int] = 5,
    handlers: Optional[Iterable[logging.Handler]] = None,
    logger: Optional[logging.Logger] = None,
    logging_classes: Iterable[Type] = DefaultLogger(),
    logging_functions: Iterable[Callable] = ()
) -> None:
    """Wraps formatters of each handler of the `logger` with the special
    `IndentingFormatter`.

    If `logger` is `None` (default), root logger will be used. If `logger`
    doesn't have any handlers added, an instance of `logging.StreamHandler`
    will be created and added.

    Handlers to be wrapped can be also provided through `handlers` argument.
    In this case `loigger` argument is not taken into consideration.

    If your application writes logs by calling custom logging functions, these
    functions should be registered in `logging_functions`. Alternatively, if
    they are methods of a class, this class can be registered in
    `logging_classes`. There is no need of registering classes that derive from
    `logging.Logger`.

    Indentation is created as `indentation * indentation_level`, where
    `indentation_level` is calculated from current location in the call stack.
    `indentation_level` can be limited by `max_level`, or unlimited when
    `max_level` is `None`. Whenever `indentation_level` exceeds the limit,
    indentation is created as
    `indentation * (max_level - 1) + deepest_indentation`.

    Arguments:
        indentation: String concatenated with the message to create a
            single-level indentation.
        deepest_indentation: String preceeding the message in case when
            indentation level exceeds the limit.
        max_level: Limit of the indentation level. Use `None` for disabling the
            limit.
        handlers: Logging handlers, formatters of which are wrapped by
            `IndentingFormatter`.
        logger: Logger, handlers of which are explored to have their formatters
            wrapped.
        logging_classes: Collection of classes, methods of which are considered
            as logging functions.
        logging_functions: Collection of logging functions.
    """

    if isinstance(logging_classes, DefaultLogger):
        logging_classes = DefaultLogger.value

    monitor = StackMonitor(logging_classes, logging_functions)

    if handlers is None:
        if logger is None:
            logger = logging.getLogger()
        if not logger.handlers:
            # Default handler (`logging.lastResort`) could be used here,
            # but it is not part of the official API
            logger.addHandler(logging.StreamHandler())
        handlers = logger.handlers

    for handler in handlers:
        ind_fmt = IndentingFormatter(monitor, indentation, deepest_indentation,
                                     max_level)
        if handler.formatter is None:
            handler.setFormatter(ind_fmt)
        else:
            stk_fmt = StackedFormatter(handler.formatter, ind_fmt)
            handler.setFormatter(stk_fmt)
