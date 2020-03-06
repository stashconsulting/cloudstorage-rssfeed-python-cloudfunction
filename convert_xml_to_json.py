"""Convert the data into the bucket and Json

and displays into the API
"""
from google.cloud import storage
from os import environ
import xmltodict
import json

storage_client = storage.Client()
destination_bucket = environ.get('DESTINATION_BUCKET', '')
bucket = storage_client.get_bucket(destination_bucket)


def convert(request):
    blob = bucket.get_blob('rssfeed.xml')
    xml_data = blob.download_as_string()
    dictionary = xmltodict.parse(xml_data)
    return json.dumps(dictionary)
