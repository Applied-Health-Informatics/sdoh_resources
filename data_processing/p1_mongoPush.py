
import os 
from dotenv import load_dotenv
import math
import pandas as pd 
import geopandas as gpd
import shapely
import json
from bson import json_util

from data_processing.mongoConnect import mongodbconnection

# Load the .env file
load_dotenv()

atlas_db_name = os.getenv("ATLAS_DB_NAME")

### Testing connection to Atlas
client = mongodbconnection()

## Create a new database and collection
collection = client["sdoh_resources"]

## load in the geojson
clean_df = gpd.read_file('data/clean/cleaned_community_partners.geojson')
len(clean_df)

## get a count of rows with missing or null geometry
clean_df.isnull().sum()

clean_df.delivery_method.value_counts()

## drop rows with missing or null geometry
# clean_df = clean_df.dropna(subset=['geometry'])
# len(clean_df)

# Convert the 'geometry' column to a GeoJSON format
def convert_to_geojson(point):
    return json.loads(json_util.dumps(shapely.geometry.mapping(point)))

## convert geometry geometry column to a geojson format
## if geometry is not null, convert to geojson, else return None

if clean_df['geometry'].isnull().sum() > 0:
    clean_df['geometry'] = clean_df['geometry'].apply(lambda x: convert_to_geojson(x) if x is not None else None)

# clean_df['geometry'] = clean_df['geometry'].apply(convert_to_geojson)

# # if value is NaN for lat and long, then set to None
# clean_df['lat'] = clean_df['lat'].apply(lambda x: None if pd.isnull(x) else x)
# clean_df['long'] = clean_df['long'].apply(lambda x: None if pd.isnull(x) else x)

clean_df.columns
clean_df.zip_code
clean_df.lat
clean_df.long
clean_df.geometry

## convert the dataframe to dictionary
clean_df_missing = clean_df.to_dict("records")

# Function to check if a value is NaN
def is_nan(value):
    return isinstance(value, float) and math.isnan(value)

# Convert None and NaN to the string 'nan'
# Convert None and NaN to the string 'nan', excluding 'geometry' key
for item in clean_df_missing:
    for key, value in item.items():
        if key != 'geometry':  # Exclude 'geometry' key from the process
            if value is None or is_nan(value):
                item[key] = 'nan'

## delete all documents in the collection
collection.delete_many({})

## confirm that the collection is empty
collection.count_documents({})

## insert the df into the collection
collection.insert_many(clean_df_missing)

## create a geospatial index that is 2dsphere and based on the geometry column
collection.create_index([("geometry", "2dsphere")])

## create an index on the zip_code column
collection.create_index("zip_code")

## return the indexes
collection.index_information()









