""" This code demonstrates insert data into firestore
using cloud Function with a http trigger
for any POST request in the API(endpoints) .
"""
from google.cloud import firestore, storage
from os import environ

client = firestore.Client()
collection = environ.get('collection', '')
storage_client = storage.Client()
destination_bucket = environ.get('DESTINATION_BUCKET', '')


def get_data(request):
    request_form = request.form
    request_files = request.files

    title = request_form['title']
    description = request_form['description']
    creation_date = request_form['creation_date']

    for key in request_files.keys():
        upload_blob(
            destination_bucket=destination_bucket,
            destination_blob_name=key,
            content=request_files[key]
        )


def upload_blob(destination_bucket, content, destination_blob_name):
    """Upload a file into the bucket destination.
    """
    bucket = storage_client.get_bucket(destination_bucket)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(content)


# def post_data():
#     data = {
#         u'title': title,
#         u'description': description,
#         u'creation_date': creation_date,
#         u'link': u'link',
#         u'generation_date': datetime.datetime.now()
#     }

#     client.collection(collection).document().set(data)
