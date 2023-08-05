from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np

class base_model:
    def __init__(self):
       print('Welcome to EMC Challenge')
    def split(self, data, label_column, train_size, seed):
        y = data[label_column]
        X = data.drop(label_column, axis = 1)
        X_train,X_test,y_train,y_test = train_test_split(X, y, train_size=train_size, random_state=seed)
        return X_train, X_test, y_train, y_test

    def split_noshuffle(self, data, label_column, train_size, seed):
        y = data[label_column]
        X = data.drop(label_column, axis = 1)
        X_train,X_test,y_train,y_test = train_test_split(X, y, train_size=train_size, random_state=seed, shuffle=False)
        return X_train, X_test, y_train, y_test
    
    def evaluation(self, y_pre, y_true):
        print("MAE : {}".format(metrics.mean_absolute_error(y_true, y_pre)))
        print("MSE : {}".format(metrics.mean_squared_error(y_true, y_pre)))
        print("RMSE : {}".format(np.sqrt(metrics.mean_squared_error(y_true, y_pre))))
        return None
