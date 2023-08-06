"""
This module contains python patterns to ease programming and usage.
"""
from __future__ import annotations
from typing import Optional

class Borg:
    """Singleton pattern Borg singleton pattern"""
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instance: Optional[Singleton] = None

    def __call__(self) -> Singleton:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance