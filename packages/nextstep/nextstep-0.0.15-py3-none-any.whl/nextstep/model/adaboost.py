from sklearn.ensemble import AdaBoostRegressor
from .base_model import base_model


class adaboost(base_model):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        print('Building adaboost model.')
        model = AdaBoostRegressor(base_estimator = self._config['base_estimator'],
                                  n_estimators = self._config['n_estimators'],
                                  learning_rate = self._config['learning_rate'],
                                  loss = self._config['loss'],
                                  random_state = self._config['seed'])
        self._model = model
        
        X_train, X_test, y_train, y_test = self.split(data,
                                                      self._config['label_column'],
                                                      self._config['train_size'],
                                                      self._config['seed'])
        
        self._model.fit(X_train, y_train)
        y_predicted = self._model.predict(X_test)

        print('Evaluating adaboost performance.')
        self.evaluation(y_test, y_predicted)
        return model
    
    def predict(self, X_new):
        return self._model.predict(X_new)
    
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("../../development/Feature_Mart/feature_mart_merged_1.csv")
    data = data.drop(['date','demand_clusters','moonrise','moonset','sunrise','sunset'], axis = 1)
    from random_forest import random_forest
    random_forest_shell = random_forest({
                                    'label_column' : 'USEP',
                                    'train_size' : 0.8,
                                    'seed' : 33,
                                    'n_estimators' : 5,
                                    'bootstrap' : True,
                                    'criterion' : 'mse',
                                    'max_features' : 'sqrt'})
    
    rf = random_forest_shell.build_model(data)
    
    user_config = {'label_column' : 'USEP',
                   'train_size' : 0.9,
                   'seed' : 33,
                   'base_estimator': rf,
                   'n_estimators' : 10,
                   'learning_rate' : 1,
                   'loss' : 'square'}
    adaboost_shell = adaboost(user_config)
    adaboost_shell.build_model(data)
    
