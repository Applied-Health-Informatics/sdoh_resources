import requests 
import pandas as pd 

## https://data.ny.gov/Economic-Development/Corporations-and-Other-Entities-All-Filings-Addres/2tms-hftb/about_data
## https://data.ny.gov/resource/2tms-hftb.json

url = 'https://data.ny.gov/resource/2tms-hftb.json'

## load up zip codes from nassau and suffolk
nassau_zipcodes = pd.read_csv('data/external/zipcodes/nassau_zipcodes.csv')
suffolk_zipcodes = pd.read_csv('data/external/zipcodes/suffolk_zipcodes.csv')

## keep only 'Zip Code' column from each, remove .0, and convert to list of strings
nassau_zipcodes = nassau_zipcodes['Zip Code'].astype(str).str.replace('.0','').tolist()
print(len(nassau_zipcodes))
suffolk_zipcodes = suffolk_zipcodes['Zip Code'].astype(str).str.replace('.0','').tolist()
print(len(suffolk_zipcodes))

## drop dups
nassau_zipcodes = list(set(nassau_zipcodes))
len(nassau_zipcodes)
suffolk_zipcodes = list(set(suffolk_zipcodes))
len(suffolk_zipcodes)

## get data from API, filter by zip codes
response_nassau = {}
nassau_zipcodes_short = nassau_zipcodes[:5]
for zipcode in nassau_zipcodes_short:
    print('Working on:', zipcode)
    response = requests.get(url + '?zip5=' + zipcode + '&$limit=50000')
    data = response.json()
    print(len(data))
    response_nassau[zipcode] = data
    


response_suffolk = {}
suffolk_zipcodes_short = suffolk_zipcodes[:5]
for zipcode in suffolk_zipcodes_short:
    print('Working on:', zipcode)
    response = requests.get(url + '?zip5=' + zipcode + '&$limit=50000')
    data = response.json()
    print(len(data))
    response_suffolk[zipcode] = data



## convert to dataframes
df_nassau = pd.DataFrame()
for zipcode in response_nassau:
    df = pd.DataFrame(response_nassau[zipcode])
    df_nassau = pd.concat([df_nassau, df])

df_suffolk = pd.DataFrame()
for zipcode in response_suffolk:
    df = pd.DataFrame(response_suffolk[zipcode])
    df_suffolk = pd.concat([df_suffolk, df])

## save to csv
df_nassau.to_csv('data/external/economic_incorporations/nassau_corporations.csv', index=False)
df_suffolk.to_csv('data/external/economic_incorporations/suffolk_corporations.csv', index=False)

