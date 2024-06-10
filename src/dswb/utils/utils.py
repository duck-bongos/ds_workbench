from typing import Generator, Tuple

import numpy as np


def f(a: int, b: int) -> float:
    """Run function f.

    Args:
        a (int): Initial integer.
        b (int): Secondary integer.

    Returns:
        float: The computed value.
    """
    return a * b * 1.0


def g(a: int, b: int) -> float:
    """Run function g.

    Args:
        a (int): Initial integer.
        b (int): Secondary integer.

    Returns:
        float: The computed value.
    """
    try:
        c = a / b
    except ZeroDivisionError:
        c = 0.0
    return c


def h(a: int, b: int) -> float:
    """Run function h.

    Args:
        a (int): Initial integer.
        b (int): Secondary integer.

    Returns:
        float: The computed value.
    """
    return f(a, g(a, b))


class Classy:
    """A classy class that does classy things.

    Example:
        >>> c = Classy()
        >>> x, y = c.generate_sample()

    """

    def generate_sample(
        self, feat_size: int = 100, label_size: int = 100
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """Generate a random sample.

        Args:
            feat_size (int, optional): Idk, doesn't matter. Defaults to 100.
            label_size (int, optional): Idk, doesn't matter. Defaults to 100.

        Yields:
            Tuple: an X and Y numpy arrays.
        """
        v = np.random.pareto(3, 29000)
        c = 29000 / v.max()
        v = (c * v).astype(int)
        x = np.stack(
            [np.random.choice(v, size=feat_size, replace=False) for _ in range(1000)]
        )
        y = np.random.randint(2, size=label_size)

        yield x, y
