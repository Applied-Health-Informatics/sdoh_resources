
import os 
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load the .env file
load_dotenv()

atlas_user = os.getenv("ATLAS_USERNAME")
atlas_password = os.getenv("ATLAS_PASSWORD")
atlas_db_name = os.getenv("ATLAS_DB_NAME")

def mongodbconnection():
    ### Testing connection to Atlas
    uri = f'mongodb+srv://{atlas_user}:{atlas_password}@cluster0.hygna83.mongodb.net/?retryWrites=true&w=majority'

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


    ## Create a new database and collection
    db = client[atlas_db_name]

    return db
