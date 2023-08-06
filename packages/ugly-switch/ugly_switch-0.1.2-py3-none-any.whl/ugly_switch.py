#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-03-15"
__version__ = "0.1.1"

__all__ = ('switch',)

"""An ugly pseudo solution for using switches in python.
There won't be any optimization or any fancy stuff,
but hey, they are reusable"""

from typing import Hashable, Dict, Tuple, Callable, Union, List


class switch:  # lowercase will probably look better in code... I guess
    cases: Dict[Hashable, Callable]
    default: Callable

    def __call__(self, item: Hashable) -> 'switch':
        try: self.cases[item]()
        except KeyError: self.default() or (lambda: None)
        finally: return self

    def __class_getitem__(cls, *cases: Tuple[Union[Hashable, Callable], ...]) -> 'switch':
        sw = cls()
        sw.set_cases(*cases)
        return sw

    def set_cases(self, *cases: Tuple[Union[Hashable, Callable], ...]) -> None:
        cases: List[Union[Hashable, Callable], ...] = list(*cases)
        if len(cases) % 2 != 0: self.default = cases.pop()  # the last item is default if len is odd
        self.cases = dict(zip(*([iter(cases)] * 2)))  # split into chunks of two, to create the dict

    def __len__(self) -> int: return len(self.cases)

    def __bool__(self) -> bool: return bool(self.cases)

    @property
    def has_cases(self) -> bool: return bool(self)

    @property
    def has_default(self) -> bool: return hasattr(self, 'default')

    def add_case(self, case: Hashable, action: Callable) -> None: self.cases.update({case: action})

    def __getitem__(self, item) -> Callable: return self.cases[item]

    def __setitem__(self, case: Hashable, action: Callable) -> None: self.add_case(case, action)

    def __repr__(self) -> str:
        return 'switch ?:\n' \
                   + '\n'.join(f'\tcase {case}: {action.__name__}' for case, action, in self.cases.items()) \
                   + (f'\n\tdefault: {self.default.__name__}' if self.has_default else '')

    __str__ = __repr__


if __name__ == '__main__': pass
