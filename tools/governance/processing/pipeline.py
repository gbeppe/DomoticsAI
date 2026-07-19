"""Generic sequential processing pipeline."""

from collections.abc import Iterable
from typing import Generic, TypeVar

from .stage import Stage


T = TypeVar("T")


class Pipeline(Generic[T]):
    """Execute a sequence of stages over a shared state object."""

    def __init__(self, stages: Iterable[Stage[T]]) -> None:
        self._stages = tuple(stages)

    @property
    def stages(self) -> tuple[Stage[T], ...]:
        """Return the immutable sequence of configured stages."""
        return self._stages

    def run(self, value: T) -> T:
        """Run every configured stage in declaration order."""
        result = value

        for stage in self._stages:
            result = stage.process(result)

        return result
