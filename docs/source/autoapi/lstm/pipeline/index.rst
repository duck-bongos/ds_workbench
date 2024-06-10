lstm.pipeline
=============

.. py:module:: lstm.pipeline


Functions
---------

.. autoapisummary::

   lstm.pipeline.make_classification
   lstm.pipeline.make_data
   lstm.pipeline.make_ragged


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