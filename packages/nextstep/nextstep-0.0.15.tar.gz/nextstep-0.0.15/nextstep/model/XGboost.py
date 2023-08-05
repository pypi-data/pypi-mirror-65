import xgboost as xgb
from base_model import base_model


class xgboost(base_model):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        print('Building xgboost model.')
        model = xgb.XGBRegressor(learning_rate = self._config['learning_rate'], 
                                      n_estimators = self._config['n_estimators'],
                                      max_depth = self._config['max_depth'],
                                      min_child_weight = self._config['min_child_weight'],
                                      gamma = self._config['gamma'],
                                      subsample=self._config['subsample'],
                                      colsample_bytree=self._config['colsample_bytree'],
                                      objective=self._config['objective'],
                                      scale_pos_weight=self._config['scale_pos_weight'])
        self._model = model

        X_train, X_test, y_train, y_test = self.split(data,
                                                      self._config['label_column'],
                                                      self._config['train_size'],
                                                      self._config['seed'])
        self._model.fit(X_train, y_train)
        y_predicted = self._model.predict(X_test)


        print('Evaluating xgboost performance.')
        self.evaluation(y_test, y_predicted)
        return model
    
    def predict(self, X_new):
        return self._model.predict(X_new)

    
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("../../../feature_mart.csv")
    data = data[-100:]
    xgboost_shell = xgboost({    
                'label_column': 'USEP',
                'train_size' : 0.8,
                'seed' : 33,
                'learning_rate': 0.1,
                'n_estimators': 150,
                'max_depth': 20,
                'min_child_weight': 4,
                'gamma': 0,
                'subsample': 0.7,
                'colsample_bytree': 0.8,
                'objective': 'reg:linear',
                'scale_pos_weight': 1,
                'seed': 1234})
    
    xgboost_shell.build_model(data)
