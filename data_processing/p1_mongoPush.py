
import os 
from dotenv import load_dotenv

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

## drop rows with missing or null geometry
clean_df = clean_df.dropna(subset=['geometry'])
len(clean_df)

# Convert the 'geometry' column to a GeoJSON format
def convert_to_geojson(point):
    return json.loads(json_util.dumps(shapely.geometry.mapping(point)))

## convert the geometry column to a geojson format
clean_df['geometry'] = clean_df['geometry'].apply(convert_to_geojson)

clean_df.columns
clean_df.zip_code

## insert the df into the collection
collection.insert_many(clean_df.to_dict("records"))

## create a geospatial index that is 2dsphere and based on the geometry column
collection.create_index([("geometry", "2dsphere")])

## create an index on the zip_code column
collection.create_index("zip_code")

## return the indexes
collection.index_information()









