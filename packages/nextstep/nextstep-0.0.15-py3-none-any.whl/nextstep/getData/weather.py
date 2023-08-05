from wwo_hist import retrieve_hist_data
import pandas as pd

class weather:
    def __init__(self, config):
        self.config = config

    def get_weather_data(self):
        retrieve_hist_data(self.config['api_key'],
                           self.config['location_list'],
                           self.config['start_date'],
                           self.config['end_date'],
                           self.config['frequency'],
                           location_label = self.config['location_label'],
                           export_csv = True,
                           store_df = False)
        return None
    def proprogate_half_hourly(self, data):
        data = data.drop_duplicates()
        # parse datetime columns
        data['date_time'] = pd.to_datetime(data['date_time'])
        # extract period and date
        data['period'] = data['date_time'].apply(lambda x:x.hour)
        data['date'] = data['date_time'].apply(lambda x:x.date())
        # parsing
        data2 = data.copy()
        data['period'] = data['period'] * 2
        data2['period'] = (data2['period'] * 2) + 1
        full = pd.concat([data,data2]).sort_values(by = ['date', 'period'])
        full["period"] = full["period"] + 1
        return full
    


if __name__ == '__main__':
    user_config = {'frequency' : 1,
                   'start_date' : '01-Jan-2010',
                   'end_date' : '31-Jan-2010',
                   'api_key' : '2c9e967a17ba475087893244201503',
                   'location_list' : ['singapore'],
                   'location_label' : False}
    
    weather_tool = weather(user_config)
    weather_tool.get_weather_data()
    data = pd.read_csv('singapore.csv')
    data = weather_tool.proprogate_half_hourly(data)
    print(len(data))
