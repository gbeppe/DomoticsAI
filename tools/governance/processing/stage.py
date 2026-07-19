"""Stage contracts used by Governance Toolkit processing pipelines."""

from typing import Protocol, TypeVar


T = TypeVar("T")


class Stage(Protocol[T]):
    """A processing step that receives and returns the pipeline state."""

    def process(self, value: T) -> T:
        """Process the current state and return the resulting state."""
        ...
