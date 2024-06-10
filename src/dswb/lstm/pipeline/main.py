from typing import Tuple, Any

from sklearn.datasets import make_multilabel_classification, make_classification
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import keras
import tensorflow as tf
from keras import Sequential
from keras.layers import (
    Attention,
    Bidirectional,
    Conv1D,
    Dense,
    Dropout,
    Flatten,
    Embedding,
    TimeDistributed,
    LSTM,
    Masking,
)
from sklearn.metrics import accuracy_score
from keras.metrics import CategoricalAccuracy

MAX_FEAT = 20000
MAX_LABELS = 14
MAX_LEN = 200


def make_data() -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    (x_train, y_train), (x_val, y_val) = keras.datasets.imdb.load_data(
        num_words=MAX_FEAT
    )
    """Generate a Keras training and validation dataset.

    Returns:
        (Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]):
            Returns a training tuple and validation tuple of the form
            (x_train, y_train), (x_val, y_val)
    """
    return (x_train, y_train), (x_val, y_val)


# x_train = keras.utils.pad_sequences(x_train, maxlen=MAX_LEN)
# x_val = keras.utils.pad_sequences(x_val, maxlen=MAX_LEN)


def make_ragged(x: np.ndarray, y: np.ndarray) -> Tuple[tf.Tensor, tf.Tensor]:
    """Transform a dense NumPy array into a ragged tensor.

    For definitions on what a ragged tensor is, please see the documentation
    on Tensorflow.

    Args:
        x (np.ndarray): The features to transform.
        y (np.ndarray): The labels to transform.

    Returns:
        Tuple[tf.Tensor, tf.Tensor]: _description_
    """
    binny = MultiLabelBinarizer()

    xt = tf.ragged.constant(x)
    yt = list(y)
    for i, x in enumerate(yt):
        if x:
            yt[i] = set(list(np.random.randint(1, 14, size=np.random.randint(1, 14))))
        else:
            yt[i] = [x]

    yeet = tf.convert_to_tensor(binny.fit_transform(yt))
    # padding taken care of in taken care of ragged -> to.tensor()
    # keras.utils.pad_sequences(yeet, maxlen=70, value=-1)
    # yeet_ = tf.ragged.constant(yeet)
    return xt.to_tensor(), yeet


def make_classification(
    xtrain: np.ndarray, ytrain: np.ndarray, xvalid: np.ndarray, yvalid: np.ndarray
) -> None:
    """Make your classifications

    Args:
        xtrain (np.ndarray): The features to train on.
        ytrain (np.ndarray): The labels to train on.
        xvalid (np.ndarray): The features to validate against.
        yvalid (np.ndarray): The labels to validate against.
    """

    # define the model
    model = Sequential(name="Dan_Lord_of_Time")
    # Input for variable-length sequences of integers
    inputs = keras.Input(shape=[None, None], dtype="int32", ragged=False)
    # Embed each integer in a 128-dimensional vector
    x = Embedding(MAX_FEAT, 4)(inputs)
    model.add(Embedding(MAX_FEAT, 4))
    # model.add(TimeDistributed(Flatten()))
    # Add 2 bidirectional LSTMs
    # model.add(Bidirectional(LSTM(4, return_sequences=True)))
    # model.add(Bidirectional(LSTM(4, return_sequences=True)))
    model.add(Bidirectional(LSTM(4, return_sequences=False)))
    # Add a classifier
    # model.add(Dense(8, activation="relu"))
    # model.add(Dropout(0.2))
    model.add(Dense(MAX_LABELS, activation="sigmoid"))
    model.summary()

    model.compile(
        optimizer=tf.keras.optimizers.Nadam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=["binary_accuracy"],
    )
    hist = model.fit(
        xtrain,
        ytrain,
        batch_size=1,
        epochs=5,
        steps_per_epoch=20,
        validation_data=(xvalid, yvalid),
    )
    print("Fit")
    print("Evaluation")
    score = model.evaluate(xvalid, yvalid, verbose=1, batch_size=1, steps=1)

    # store result
    print("Accuracy> %.3f" % score)


def main():
    (x_train, y_train), (x_val, y_val) = make_data()

    xt, yt = make_ragged(x_train, y_train)
    xv, yv = make_ragged(x_val, y_val)

    maxlen = max([len(x) for x in xt])

    xv, yv = make_ragged(x_val, y_val)

    return make_classification(xtrain=xt, ytrain=yt, xvalid=xv, yvalid=yv)


if __name__ in "__main__":
    main()
