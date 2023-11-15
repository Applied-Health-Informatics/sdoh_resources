from flask import Flask, render_template, request
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
      
        query = {
            "geometry": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": center_coordinates
                    },
                    "$maxDistance": distance_meters
                }
            }
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
                               results=results_list, 
                               category_counts=unique_categories_with_counts,
                               results_json=results_json,
                               zipcode=zip_code, 
                               distance=distance_miles)     


    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
