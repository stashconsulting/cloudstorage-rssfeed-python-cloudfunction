""" This code demonstrates writing, deploying, and triggering a

Cloud Function with a Cloud Firestore trigger

for any change to a specific document .
"""
from xml.etree.ElementTree import Element, SubElement, \
    Comment, tostring
from xml.dom import minidom
from google.cloud import firestore, storage
from os import environ

# collection_name = environ.get('food-details')
destination_bucket = environ.get('DESTINATION_BUCKET', '')
database_client = firestore.Client()
storage_client = storage.Client()


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def gather_items(parent_element):
    """Search into firestore database in the cloud

    to scrap the title, name, link, creation and generation date.
    """
    docs = database_client.collection(u'food-details').stream()
    for doc in docs.iteritems():
        _, dict_values = doc.to_dict()
        item = SubElement(parent_element, 'item')

        title = SubElement(item, 'title')
        title.text = dict_values['title']

        link = SubElement(item, 'link')
        link.text = dict_values['link']

        description = SubElement(item, 'description')
        description.text = dict_values['description']

        date_creation = SubElement(item, 'Date')
        date_creation.text = dict_values['creation_date']

        upload = SubElement(item, 'upload')
        upload.text = dict_values['generation_date']


def upload_blob(destination_bucket, content, destination_blob_name):
    """Upload a file into the bucket destination.
    """
    bucket = storage_client.get_bucket(destination_bucket)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content)


def main(event, context):
    """Write the file.
    """
    channel = Element('channel')
    title = SubElement(channel, 'title')
    title.text = "podcasts"
    comment = Comment('Generated for Learning')
    channel.append(comment)
    gather_items(channel)
    upload_blob(
        destination_bucket,
        prettify(channel),
        'rssfeed.xml'
    )
