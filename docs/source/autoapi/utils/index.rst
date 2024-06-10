utils
=====

.. py:module:: utils


Classes
-------

.. autoapisummary::

   utils.Classy


Functions
---------

.. autoapisummary::

   utils.f
   utils.g
   utils.h


Package Contents
----------------

.. py:function:: f(a: int, b: int) -> float

   Run function f.

   Args:
       a (int): Initial integer.
       b (int): Secondary integer.

   Returns:
       float: The computed value.


.. py:function:: g(a: int, b: int) -> float

   Run function g.

   Args:
       a (int): Initial integer.
       b (int): Secondary integer.

   Returns:
       float: The computed value.


.. py:function:: h(a: int, b: int) -> float

   Run function h.

   Args:
       a (int): Initial integer.
       b (int): Secondary integer.

   Returns:
       float: The computed value.


.. py:class:: Classy

   A classy class that does classy things.

   Example:
       >>> c = Classy()
       >>> x, y = c.generate_sample()



   .. py:method:: generate_sample(feat_size: int = 100, label_size: int = 100) -> Generator[Tuple[numpy.ndarray, numpy.ndarray], None, None]

      Generate a random sample.

      Args:
          feat_size (int, optional): Idk, doesn't matter. Defaults to 100.
          label_size (int, optional): Idk, doesn't matter. Defaults to 100.

      Yields:
          Tuple: an X and Y numpy arrays.




.. toctree::