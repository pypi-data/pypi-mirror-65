from sklearn.ensemble import RandomForestRegressor
from .base_model import base_model


class random_forest(base_model):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        print('Building random forest model.')
        model = RandomForestRegressor(n_estimators = self._config['n_estimators'], 
                                      bootstrap = self._config['bootstrap'],
                                      criterion = self._config['criterion'],
                                      max_features = self._config['max_features'])
        self._model = model

        X_train, X_test, y_train, y_test = self.split(data,
                                                      self._config['label_column'],
                                                      self._config['train_size'],
                                                      self._config['seed'])
        self._model.fit(X_train, y_train)
        y_predicted = self._model.predict(X_test)
        
        print('Evaluating random forest performance.')
        self.evaluation(y_test, y_predicted)
        return model
    
    def predict(self, X_new):
        return self._model.predict(X_new)

    
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("../../development/Feature_Mart/feature_mart_merged_1.csv")
    data = data.drop(['date','demand_clusters','moonrise','moonset','sunrise','sunset'], axis = 1)
    random_forest_shell = random_forest({
                                    'label_column' : 'USEP',
                                    'train_size' : 0.8,
                                    'seed' : 33,
                                    'n_estimators' : 5,
                                    'bootstrap' : True,
                                    'criterion' : 'mse',
                                    'max_features' : 'sqrt'})
    
    random_forest_shell.build_model(data)
