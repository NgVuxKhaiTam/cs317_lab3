import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Masking, TimeDistributed
from typing import List

# input_shape = (sequence_length, train_array.shape[2])
def create_model(input_shape, nodes_per_layer: List, dropout: int, activation: str, weights_file: str):
    """
        Creates an LSTM model using the Keras Sequential API.

        Parameters:
        - input_shape: tuple
            The shape of the input data, usually (sequence_length, num_features)
        - nodes_per_layer: list[int]
            A list specifying the number of neurons for each LSTM layer. For example, [50] or [50, 20]
        - dropout: float
            The dropout rate applied after each LSTM layer (e.g., 0.2)
        - activation: str
            The activation function used in the LSTM layers (e.g., 'tanh', 'relu')
        - weights_file: str
            The file path to save the model weights after initialization

        Returns:
        - model: tensorflow.keras.Model
            The compiled Keras model ready for training
    """
    model = Sequential()
    model.add(Masking(mask_value=-99., input_shape=input_shape))
    if len(nodes_per_layer) <= 1:
        model.add(LSTM(nodes_per_layer[0], activation=activation))
        model.add(Dropout(dropout))
    else:
        model.add(LSTM(nodes_per_layer[0], activation=activation, return_sequences=True))
        model.add(Dropout(dropout))
        model.add(LSTM(nodes_per_layer[1], activation=activation))
        model.add(Dropout(dropout))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.save_weights(weights_file)
    return model