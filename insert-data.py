""" This code demonstrates insert data into firestore

using cloud Function with a http trigger

for any POST request in the API(endpoints) .
"""
from google.cloud import firestore
import datetime

client = firestore.Client()
collection = u'food-details'


def get_data(request):
    request_json = request.get_json()
    title = request_json['title']
    description = request_json['description']
    creation_date = request_json['creation_date']
    data = {
        u'title': title,
        u'description': description,
        u'creation_date': creation_date,
        # u'link': u'link',
        u'generation_date': datetime.datetime.now()
    }
    client.collection(collection).document().set(data)
