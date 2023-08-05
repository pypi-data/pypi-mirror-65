from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_pacf
from .base_model import base_model
import pandas as pd
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


class arima(base_model):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        print('Building arima model.')

        size = int(len(data) * self._config['train_size'])
        data = data[self._config['label_column']].values
        train, test = data[:size].tolist(), data[size:]

        model = ARIMA(train,
                        order=(self._config['lag'], self._config['differencing'], self._config['window_size']))
        fitted_model = model.fit()
        
        predictions = fitted_model.forecast(steps = len(test))[0]
        
        print('Evaluating arima performance.')
        self.evaluation(test, predictions)

        model = ARIMA(data,
                      order=(self._config['lag'], self._config['differencing'], self._config['window_size']))
        model_fitted = model.fit()
        self._model = model_fitted
        return model
    
    def predict(self, X_new):
        return self._model.predict(X_new)
    
    def predict_next_n(self, step):
        return self._model.forecast(steps = step)[0]

    def autocorrelation(self, data, number_of_time_step = 20):
        print("Autocorrelation")
        try:
            autocorrelation_plot(data[self._config['label_column']][:number_of_time_step])
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter number of time step. to be below 20.')
        return None
    
    def partial_autocorrelation(self, data, lags = 20):
        print("Partial Autocorrelation")
        try:
            plot_pacf(data[self._config['label_column']], lags = lags)
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter lags to be below 20.')
        return None
    
    def residual_plot(self):
        print("Residual Plot")
        df = pd.DataFrame(self._model.resid)
        df.plot()
        df.plot(kind='kde')
        pyplot.show()
        print("residual mean is {}".format(sum(self._model.resid)/len(self._model.resid)))
        return None
    
    def residual_density_plot(self):
        print("Residual Density Plot")
        pd.DataFrame(self._model.resid).plot(kind='kde')
        pyplot.show()
        return None        
        
    
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("../../../feature_mart.csv")
    data = data[-100:]
    
    user_config = {'lag' : 2,
                   'differencing' : 0,
                   'window_size' : 2,
                   'label_column' : 'USEP',
                   'train_size' : 0.8,
                   'seed' : 33}
    arima_shell = arima(user_config)
##    arima_shell.autocorrelation(data)
##    arima_shell.partial_autocorrelation(data)
    arima_shell.build_model(data)
    print(arima_shell.predict_next_n(10))
##    arima_shell.residual_plot()
    
