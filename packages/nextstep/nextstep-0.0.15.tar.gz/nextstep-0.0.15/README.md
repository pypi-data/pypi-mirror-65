
# nextstep

# Introduction
Nextstep integrates major popular machine learning algorithms, offering data scientists an all-in-one package. At the same time, it lifts the programming constraints by extracting key hyper-parameters into a configuration dictionary, empowering less experienced python users the ability to explore machine learning. 

Nextstep was originally developed for a data science challenge which involved price prediction. So it has a dedicated module to obtain data (oil and weather) via open API or web-scraping. It evolves into a machine learning prediction toolkit.

# Installation
First time installation
```bash
pip install nextstep
```
Upgrade to the latest version
```bash
pip install nextstep --upgrade
```
# Quick Tutorial
## getData module
**generate oil prices**
```python
from nextstep.getData.oil import *
oil_prices.process()
```
*brent_daily.csv* and *wti_daily.csv* will be generated at the current directory. They contain historical oil price until the most recent day.

**generate weather data**

This function relies on an API key from [worldweatheronline](https://www.worldweatheronline.com/developer/). It is free for 60 days as of 27/3/2020. It will generate csv data files in the current directory.
```python
from nextstep.getData.weather import weather
config = {
		'frequency' : 1,
		'start_date' : '01-Jan-2020',
		'end_date' : '31-Jan-2020',
		'api_key' : 'your api key here',
		'location_list' : ['singapore'],
		'location_label' : False
		}
data = weather(config).get_weather_data()
```
## model module
Every ML model has a unique config. Please fill in accordingly.
### random forest
```python
# examples, please fill in according to your project scope
from nextstep.model.random_forest import random_forest
config = {
            'label_column' : 'USEP',
            'train_size' : 0.9,
            'seed' : 66,
            'n_estimators' : 10,
            'bootstrap' : True,
            'criterion' : 'mse',
            'max_features' : 'sqrt'
	}
random_forest_shell = random_forest(config)

random_forest_shell.build_model(data) # build model
```

### arima
```python
from nextstep.model.arima import arima
config = {
		'lag' : 7,
		'differencing' : 0,
		'window_size' : 2,
		'label_column' : 'USEP',
		'train_size' : 0.8,
		'seed' : 33
	}
arima_shell = arima(config)

arima_shell.autocorrelation(data) # plot autocorrelation to determine p, lag order
arima_shell.partial_autocorrelation(data) # plot partial autocorrelation to determine q, moving average widow size
arima_shell.build_model(data) # build model

# residual plot to check model performance
arima_shell.residual_plot()
arima_shell.residual_density_plot()
```

# Contributing
Pull requests are welcome

# Author
yuesong Yang