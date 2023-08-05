import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from matplotlib import pyplot
from .base_model import base_model
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


class sarima(base_model):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        print('Building sarima model.')

        size = int(len(data) * self._config['train_size'])
        data = data[self._config['label_column']].values
        train, test = data[:size].tolist(), data[size:]
        
        model = SARIMAX(train,
                        order=(self._config['trend_order'][0], self._config['trend_order'][1], self._config['trend_order'][2]),
                        seasonal_order=(self._config['season_order'][0], self._config['season_order'][1], self._config['season_order'][2], self._config['season_order'][3])
                        )
        fitted_model = model.fit()
        
        predictions = fitted_model.forecast(steps = len(test))

        print('Evaluating arima performance.')
        self.evaluation(test, predictions)

        model = SARIMAX(train,
                      order=(self._config['trend_order'][0], self._config['trend_order'][1], self._config['trend_order'][2]),
                      seasonal_order=(self._config['season_order'][0], self._config['season_order'][1], self._config['season_order'][2], self._config['season_order'][3])
                      )
        model_fitted = model.fit()
        self._model = model_fitted
        return model
    
    def predict(self, X_new):
        return self._model.forecast(steps = step)

    def predict_next_n(self, steps):
        return self._model.get_forecast(steps=steps).predicted_mean

    def autocorrelation(self, data, lags = 20):
        print("Autocorrelation:")
        try:
            plot_acf(data[self._config['label_column']], lags = lags)
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter lags to be below 20.')
        return None
    
    def partial_autocorrelation(self, data, lags = 20):
        print("Partial Autocorrelation:")
        try:
            plot_pacf(data[self._config['label_column']], lags = lags)
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter lags to be below 20.')
        return None
    
    def residual_plot(self):
        print("Residual Plot:")
        df = pd.DataFrame(self._model.resid)
        df.plot()
        df.plot(kind='kde')
        pyplot.show()
        print("residual mean is {}".format(sum(self._model.resid)/len(self._model.resid)))
        return None
    
    def residual_density_plot(self):
        print("Residual Density Plot:")
        pd.DataFrame(self._model.resid).plot(kind='kde')
        pyplot.show()
        return None        
        
    
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("../../../feature_mart.csv")
    data = data[-500:]
    
    user_config = {
                   'label_column' : 'USEP',
                   'train_size' : 0.95,
                   'seed' : 33,
                   'trend_order' : (1, 1, 1),
                   'season_order' : (1, 0, 1, 48)
                   }
    sarima_shell = sarima(user_config)

##    sarima_shell.autocorrelation(data)
##    sarima_shell.partial_autocorrelation(data)
    sarima_shell.build_model(data)
    print(sarima_shell.predict_next_n(10))
    
