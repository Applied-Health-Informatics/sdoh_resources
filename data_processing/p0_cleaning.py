import pandas as pd 
import geopandas as gpd

raw_df = pd.read_excel('data/raw/Clean Community Partners Info.xlsx')

## quick cleaning 
raw_df.columns
raw_df.columns = raw_df.columns.str.replace(' ', '_').str.lower()

## lets create a point geometry column based on the 
## first lets split the coordinates column into two columns
raw_df[['lat', 'long']] = raw_df['coordinates'].str.split(',', expand=True)

## now lets convert the lat and long columns to floats
raw_df['lat'] = raw_df['lat'].astype(float)
raw_df['long'] = raw_df['long'].astype(float)

## now lets create a point geometry column
raw_df['geometry'] = gpd.points_from_xy(raw_df['long'], raw_df['lat'])

## now lets convert the dataframe to a geodataframe
raw_df = gpd.GeoDataFrame(raw_df, geometry='geometry')

## now lets save the dataframe as a geojson
raw_df.to_file('data/clean/cleaned_community_partners.geojson', driver='GeoJSON')
