from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from .base_model import base_model
import numpy as np
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

class lstm_univariate(base_model):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._model = None

    def split_sequence(self, sequence, n_steps):
        X, y = [], []
        for i in range(len(sequence)):
            end_ix = i + n_steps
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)
    
    def build_model(self, data):
        print('Building LSTM model.')
        X, y = self.split_sequence(data[self._config['label_column']], self._config['n_steps'])
        size = int(len(data) * self._config['train_size'])
        X_train = X[:size]
        y_train = y[:size]
        X_test = X[size:]
        y_test = y[size:]

        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        
        model = Sequential()
        model.add(LSTM(self._config['n_neuron'],
                       activation = self._config['activation'],
                       input_shape = (self._config['n_steps'], 1)
                       )
                  )
        model.add(Dense(1))
        
        model.compile(optimizer=self._config['optimizer'],
                      loss=self._config['loss'])
        
        model.fit(X_train,
                  y_train,
                  epochs=self._config['n_epochs'],
                  verbose=1)
        
        self._model = model

        predict = []
        for x in X_test:
            x = x.reshape((1, self._config['n_steps'], 1))
            yhat = model.predict(x, verbose=0)
            predict.append(yhat[0])
        
        print('Evaluating LSTM performance.')
        self.evaluation(y_test, predict)
        return model
    
    def predict(self, X_new):
        return self._model.predict(X_new)

    
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("../../feature_mart.csv")
    user_config = {'label_column' : 'USEP',
                   'n_steps' : 7,
                   'train_size' : 0.8,
                   'n_neuron' : 5,
                   'activation' : 'relu',
                   'optimizer' : 'adam',
                   'loss' : 'mse',
                   'n_epochs' : 2}
    
    LSTM_shell = lstm_univariate(user_config)
    LSTM_shell.build_model(data)
