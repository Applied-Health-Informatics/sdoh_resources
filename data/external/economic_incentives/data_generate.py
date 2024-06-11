import pandas as pd 
import requests 


url = 'https://data.ny.gov/resource/26ei-n4eb.json'


## nassau count 
url = 'https://data.ny.gov/resource/26ei-n4eb.json?county=Nassau&$limit=100000'
nassau = requests.get(url).json()
nassau_df = pd.DataFrame(nassau)
nassau_df.to_csv('data/external/economic_incentives/nassau_economic_incentives.csv', index=False)

## suffolk count
url = 'https://data.ny.gov/resource/26ei-n4eb.json?county=Suffolk&$limit=100000'
suffolk = requests.get(url).json()
suffolk_df = pd.DataFrame(suffolk)
suffolk_df.to_csv('data/external/economic_incentives/suffolk_economic_incentives.csv', index=False)
