from flask import Flask, render_template, request, url_for
from mongoConnect import mongodbconnection
from dotenv import load_dotenv
import json
import requests
import urllib.parse
import os

# Load the .env file
load_dotenv()

## connect to the database
client = mongodbconnection()
collection = client["sdoh_resources"]

## get unique values of filter_tags
unique_filter_tags = collection.distinct("filter_tags")
print('Unique Tags: ', unique_filter_tags)

## get the bounds of a zip code
search = 'https://maps.googleapis.com/maps/api/geocode/json?address='
api_key = os.getenv("GOOGLE_MAPS_API")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        # get form data
        zip_code = request.form['zipcode']  
        distance = request.form['distance']
        category_response = request.form['category']

        # if cateogry_response is '' then set to all categories
        if category_response == 'all':
            category_response = unique_filter_tags
            print('Category Response New: ', category_response)
            
        # ensure distance is an integer
        distance_miles = int(distance)

        # convert distance (miles) to meters
        distance_meters = distance_miles * 1609.34

        # convert location to url friendly string
        location = urllib.parse.quote(zip_code)
        url = search + location + '&key=' + api_key

        # get response
        response = requests.get(url)
        response.json()

        ## get geometry bounds
        partialPolygon = response.json()['results'][0]['geometry']['bounds']   

        # Calculate the midpoint by first getting the northeast and southwest points
        northeast = partialPolygon['northeast']
        southwest = partialPolygon['southwest']

        # Now calculate the midpoint
        center_lat = (northeast['lat'] + southwest['lat']) / 2
        center_lng = (northeast['lng'] + southwest['lng']) / 2

        # Reverse center coordinates
        center_coordinates = (center_lng, center_lat)
        
        # Convert to list
        center_coordinates = list(center_coordinates)
      

        # query database if category_response is a list
        if isinstance(category_response, list):
            query = {
                "geometry": {
                    "$near": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": center_coordinates
                        },
                        "$maxDistance": distance_meters
                    }
                },
                "filter_tags": {
                    "$in": category_response
                }
            }
        # query database if category_response is a string
        else:
            query = {
                "geometry": {
                    "$near": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": center_coordinates
                        },
                        "$maxDistance": distance_meters
                    }
                },
                "filter_tags": category_response
            } 

        results = collection.find(query)

        ## convert results to list
        results_list = list(results)

        ## convert results to json
        results_json = json.dumps(results_list, default=str)

        print("JSON RESULTS: ", results_json)

        ## get a count of unique categories
        categories = []
        for result in results_list:
            categories.append(result['filter_tags'])
        
        ## get unique categories
        unique_categories = set(categories)
        print(unique_categories)

        ## get unique categories with counts
        unique_categories_with_counts = {}
        for category in unique_categories:
            unique_categories_with_counts[category] = categories.count(category)
        print(unique_categories_with_counts)

        return render_template('index.html', 
                               unique_filter_tags=unique_filter_tags,
                               results=results_list, 
                               category_counts=unique_categories_with_counts,
                               category_response=category_response,
                               results_json=results_json,
                               zipcode=zip_code, 
                               distance=distance_miles)     


    else:
        return render_template(
            'index.html',
            unique_filter_tags=unique_filter_tags,
            )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
