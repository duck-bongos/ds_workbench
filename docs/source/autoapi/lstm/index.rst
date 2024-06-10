lstm
====

.. py:module:: lstm


Subpackages
-----------

.. toctree::
   :maxdepth: 1

   /autoapi/lstm/pipeline/index


Functions
---------

.. autoapisummary::

   lstm.make_classification
   lstm.make_data
   lstm.make_ragged


Package Contents
----------------

.. py:function:: make_classification(xtrain: numpy.ndarray, ytrain: numpy.ndarray, xvalid: numpy.ndarray, yvalid: numpy.ndarray) -> None

   Make your classifications

   Args:
       xtrain (np.ndarray): The features to train on.
       ytrain (np.ndarray): The labels to train on.
       xvalid (np.ndarray): The features to validate against.
       yvalid (np.ndarray): The labels to validate against.


.. py:function:: make_data() -> Tuple[Tuple[numpy.ndarray, numpy.ndarray], Tuple[numpy.ndarray, numpy.ndarray]]

.. py:function:: make_ragged(x: numpy.ndarray, y: numpy.ndarray) -> Tuple[tensorflow.Tensor, tensorflow.Tensor]

   Transform a dense NumPy array into a ragged tensor.

   For definitions on what a ragged tensor is, please see the documentation
   on Tensorflow.

   Args:
       x (np.ndarray): The features to transform.
       y (np.ndarray): The labels to transform.

   Returns:
       Tuple[tf.Tensor, tf.Tensor]: _description_



.. toctree::