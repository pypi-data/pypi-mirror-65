import pandas as pd

class feature_engineering:
    def __init__(self):
        print('successfully substantiate feature engineering class.')

    def concat_columns(self, dataframe_list):
        return pd.concat(dataframe_list, axis=1)

    def concat_rows(self, dataframe_list):
        return pd.concat(dataframe_list)

    def join(self, dataframe_list, on = None, how = None):
        main_df = dataframe_list[0]
        for df in dataframe_list[1:]:
            main_df = main_df.merge(df, on = on, how = how)
        return main_df
    
    def parse_datetime(self, data, datetime_col, remove = True):
        try:
            data[datetime_col] = pd.to_datetime(data[datetime_col])
        except:
            print('Not date column')
        try:
            data['year'] = data[datetime_col].apply(lambda x: x.year)
        except:
            print('No information on YEAR')
        try:
            data['month'] = data[datetime_col].apply(lambda x:x.month)
        except:
            print('No information on MONTH')
        try:
            data['day'] = data[datetime_col].apply(lambda x:x.day)
        except:
            print('No information on DAY')
        if remove:
            return data.drop(datetime_col, axis = 1)
        else:
            return data
        
    def get_dummies(self, data, column_list):
        for col in column_list:
            data = self.concat_columns([data.drop(col, axis=1), pd.get_dummies(data[col])])
        return data

    def get_weekday(self, data):
        pass
    def get_peak_offpeak_shoulder():
        pass
    
if __name__ == '__main__':
    import pandas as pd
    demand = pd.read_csv('../development/Feature_Mart/demand_feature_mart.csv')
    weather = pd.read_csv('../development/Feature_Mart/weather_feature_mart.csv')
    FE = feature_engineering()
    df = FE.join([demand, weather], on = ['date', 'period'], how ='left')
    df = FE.parse_datetime(df, 'date', remove = True)
    df = FE.get_dummies(df, 'demand_clusters')
    print(df['off-peak'])
    print(df.columns)
                


