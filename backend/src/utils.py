from typing import List, Iterator, TypeVar

T = TypeVar('T')


def chunked(iterable: List[T], size: int) -> Iterator[List[T]]:
    """Split an iterable into chunks of specified size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]