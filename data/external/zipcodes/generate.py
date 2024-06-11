import requests 
import pandas as pd 

## using pandas, pull table from https://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ny&StName=&StFIPS=&FIPS=36059
url = 'https://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ny&StName=&StFIPS=&FIPS=36059'
zipcodes_list = pd.read_html(url)
dataframes = zipcodes_list[1:]
zipcodes_df = pd.concat(dataframes, ignore_index=True)
zipcodes_df = zipcodes_df.dropna(how='all')
zipcodes_df['Zip Code']
zipcodes_df = zipcodes_df.drop(0)
zipcodes_df = zipcodes_df.drop(columns=[0,1,2,3])
## save
zipcodes_df.to_csv('data/external/zipcodes/nassau_zipcodes.csv', index=False)


## using pandas, pull table from https://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?zip=117
url = 'https://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?zip=117'
zipcodes_list = pd.read_html(url)
dataframes = zipcodes_list[1:]
zipcodes_df = pd.concat(dataframes, ignore_index=True)
zipcodes_df = zipcodes_df.dropna(how='all')
zipcodes_df['Zip Code']
zipcodes_df = zipcodes_df.drop(0)
zipcodes_df = zipcodes_df.drop(columns=[0,1,2,3,4,5])
## save
zipcodes_df.to_csv('data/external/zipcodes/suffolk_zipcodes.csv', index=False)




