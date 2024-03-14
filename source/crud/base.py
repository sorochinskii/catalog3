from abc import ABC, abstractmethod
from typing import Any, Callable


class CRUD():
    @abstractmethod
    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError
