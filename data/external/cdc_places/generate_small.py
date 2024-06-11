import pandas as pd 

df = pd.read_csv('/Users/hantswilliams/Development/python/sdoh_resources/data/external/cdc_places/ny_places2023.csv')

df.columns

## print each CountyName
df.CountyName.unique()

## keep only where CountyName is Nassau or Suffolk
longisland = df[(df['CountyName'] == 'Nassau') | (df['CountyName'] == 'Suffolk')]

## save to data/external/cdc_places/longisland_cdc_places.csv
longisland.to_csv('/Users/hantswilliams/Development/python/sdoh_resources/data/external/cdc_places/longisland_cdc_places.csv', index=False)