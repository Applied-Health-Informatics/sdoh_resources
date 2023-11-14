
from data_processing.mongoConnect import mongodbconnection
import requests
import urllib.parse
import os

## connect to the database
client = mongodbconnection()
collection = client["sdoh_resources"]



## get the bounds of a zip code
search = 'https://maps.googleapis.com/maps/api/geocode/json?address='
location = '11968'
api_key = os.getenv("GOOGLE_MAPS_API")

# convert location to url friendly string
location = urllib.parse.quote(location)
url = search + location + '&key=' + api_key

# get response
response = requests.get(url)
response.json()

## get geometry bounds
partialPolygon = response.json()['results'][0]['geometry']['bounds']






######## Approach 1 - involves a max distance, 
### takes the two points of the bounds and calculates the midpoint
### this then allows us to query using a point coordinate, which can 
### then take a max distance
northeast = partialPolygon['northeast']
southwest = partialPolygon['southwest']

# Calculate the midpoint
center_lat = (northeast['lat'] + southwest['lat']) / 2
center_lng = (northeast['lng'] + southwest['lng']) / 2

# Reverse center coordinates
center_coordinates = (center_lng, center_lat)
# convert to list
center_coordinates = list(center_coordinates)

# ## perform a geospatial query for a test for a point
query = {
    "geometry": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": center_coordinates
            },
            "$maxDistance": 16000 # 8000 meters is ~ 5 miles, 4000 meters is ~ 2.5 miles, 16000 meters is ~ 10 miles
        }
    }
}
## perform the query
results = collection.find(query)
## print the results
length = 0
for result in results:
    length += 1
    print(result)
print('Total sites found: ', length)







#### Approach 2 - doesn't involve a max distance
### takes the four points of the bounds and creates a polygon
### then this allows us to query using a polygon
### and only return the sites that are within the polygon
northeast = partialPolygon['northeast']
southwest = partialPolygon['southwest']
northwest = {'lat': northeast['lat'], 'lng': southwest['lng']}
southeast = {'lat': southwest['lat'], 'lng': northeast['lng']}

coordinates = [
    [northwest['lng'], northwest['lat']], 
    [northeast['lng'], northeast['lat']], 
    [southeast['lng'], southeast['lat']], 
    [southwest['lng'], southwest['lat']], 
    [northwest['lng'], northwest['lat']]
    ]

# Construct the query
query = {
    "geometry": {
        "$geoWithin": {
            "$geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            },
        }
    },
}

## perform the query
results = collection.find(query)
## print the results
for result in results:
    print(result)







## perform a query for a zip code
query = {
    "zip_code": "11738"
}

## perform the query
results = collection.find(query)
## print the results
for result in results:
    print(result)



# ## perform a geospatial query for a test for a point
query = {
    "geometry": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [-73.015995, 40.84436]
            },
            "$maxDistance": 8000 # 8000 meters is ~ 5 miles
        }
    }
}
## perform the query
results = collection.find(query)
## print the results
length = 0
for result in results:
    length += 1
    print(result)
print('Total sites found: ', length)