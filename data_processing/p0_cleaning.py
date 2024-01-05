import pandas as pd 
import geopandas as gpd

# raw_df = pd.read_excel('data/raw/Clean Community Partners Info.xlsx')
# raw_df = pd.read_excel('data/raw/Clean Community Partners Info with delivery methods.xlsx')
raw_df = pd.read_excel('data/raw/Clean Community Partners 2.3.xlsx')

## quick cleaning 
raw_df.columns
raw_df.columns = raw_df.columns.str.replace(' ', '_').str.lower()

raw_df.columns

exclude_columns = ['coordinates', 'lat', 'long']

# Loop through each column in the DataFrame
for column in raw_df.columns:
    # Skip the columns that are in the exclude list
    if column in exclude_columns:
        continue
    # Ensure the column is of type string
    raw_df[column] = raw_df[column].astype(str)
    # # Remove any special characters, but keep spaces, hyphens, periods, forward slashes, backward slashes, and apostrophes
    # raw_df[column] = raw_df[column].str.replace('[^a-zA-Z0-9 \'-/\\\]', '')
    # Optional: Escape apostrophes for HTML/JavaScript compatibility
    raw_df[column] = raw_df[column].str.replace('\'', '')
    # Replace 's with an empty string
    raw_df[column] = raw_df[column].str.replace('\'s', '')
    # Replace multiple spaces with a single space
    raw_df[column] = raw_df[column].str.replace(r'\s+', ' ', regex=True)


# ## for the filter_tags responses, remove any special characters, include ' and -
# raw_df['filter_tags'] = raw_df['filter_tags'].str.replace('[^a-zA-Z0-9 \'-]', '')
# raw_df['filter_tags'] = raw_df['filter_tags'].str.replace('\'s', '')
# raw_df['filter_tags'] = raw_df['filter_tags'].str.replace('  ', ' ')
# raw_df.filter_tags.value_counts()

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

raw_df['delivery_method'].value_counts()

## now lets save the dataframe as a geojson
raw_df.to_file('data/clean/cleaned_community_partners.geojson', driver='GeoJSON')


