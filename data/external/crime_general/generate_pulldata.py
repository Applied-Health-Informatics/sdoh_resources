import requests 
import pandas as pd 

## data: https://data.ny.gov/Public-Safety/Index-Crimes-by-County-and-Agency-Beginning-1990/ca8h-8gjq/about_data 

url = 'https://data.ny.gov/resource/ca8h-8gjq.json' 

nassau = 'https://data.ny.gov/resource/ca8h-8gjq.json?county=Nassau'
nassau = requests.get(nassau).json()
nassau_df = pd.DataFrame(nassau)
nassau_df.to_csv('data/external/crime_general/nassau_crime.csv', index=False)

suffolk = 'https://data.ny.gov/resource/ca8h-8gjq.json?county=Suffolk'
suffolk = requests.get(suffolk).json()
suffolk_df = pd.DataFrame(suffolk)
suffolk_df.to_csv('data/external/crime_general/suffolk_crime.csv', index=False)
