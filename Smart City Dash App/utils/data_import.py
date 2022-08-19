import pandas as pd
import pytz

# set timezone
timezone = pytz.timezone('Europe/Berlin')

# define color
bg_color = '#323232'
txt_color = 'white'
color_list = ['#8feaf2', '#f4d44d', '#ff902e', '#05f766', '#9dbefc']

# import data
df_full = pd.read_csv('./data/201911081702_SmartCityDemo.csv', index_col = 0)
df_full.index = pd.to_datetime(df_full.index)
# convert timezone to germany
df_full.index = df_full.index.tz_localize(pytz.utc).tz_convert(timezone)
df_full = df_full.resample('1H').interpolate()