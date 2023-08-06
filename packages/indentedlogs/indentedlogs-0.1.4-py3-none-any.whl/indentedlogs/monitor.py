import inspect
import operator
from abc import ABC, abstractmethod
from itertools import takewhile
from typing import Callable, Collection, Iterable, List, Type

from .utils import func_in_frame_info


class Monitor(ABC):
    @abstractmethod
    def get_level(self) -> int:
        pass


class StackMonitor(Monitor):
    def __init__(self,
                 logging_classes: Iterable[Type] = (),
                 logging_functions: Iterable[Callable] = ()):
        self._last_identifiers: Collection = tuple()
        self._identifier_groups: List = []
        logger_methods = [
            m for c in logging_classes for m in vars(c).values()
            if inspect.isfunction(m)
        ]
        self._logging_functions = (*logger_methods, *logging_functions)

    def get_level(self) -> int:
        reversed_stack = reversed(inspect.stack())
        user_stack = takewhile(self._corresponds_to_user_functon,
                               reversed_stack)
        identifiers = tuple(
            id(frame_info.frame.f_code) for frame_info in user_stack)
        return self._get_level(identifiers)

    def _corresponds_to_user_functon(self,
                                     frame_info: inspect.FrameInfo) -> bool:
        return func_in_frame_info(frame_info) not in self._logging_functions

    def _get_level(self, identifiers: Collection) -> int:

        common_part = takewhile(lambda pair: operator.eq(*pair),
                                zip(self._last_identifiers, identifiers))
        common_len = sum(1 for _ in common_part)
        identifiers_len = len(identifiers)
        last_identifiers_len = len(self._last_identifiers)

        if common_len == last_identifiers_len:
            if identifiers_len > last_identifiers_len:  # [Next level]
                self._identifier_groups.append(identifiers_len)
            # else: [Same level]

        elif common_len < last_identifiers_len:
            if common_len < identifiers_len:  # [Jump]
                selector = lambda x: x <= common_len  # noqa: E731
            else:  # [Previous level]
                selector = lambda x: x < common_len  # noqa: E731

            self._identifier_groups = list(
                takewhile(selector, self._identifier_groups))
            self._identifier_groups.append(identifiers_len)

        self._last_identifiers = identifiers
        level = len(self._identifier_groups) - 1

        return level
