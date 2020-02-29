""" This code demonstrates writing, deploying, and triggering a 

Cloud Function with a Cloud Storage trigger when 

a "write" of a Cloud Storage Object is successfully finalized.
"""
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from google.cloud import storage
from os import environ

bucket_name = environ.get('BUCKET_NAME','')
folder_name = environ.get('FOLDER_NAME', '')
storage_client = storage.Client()

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def gather_items(parent_element, data):
    """Search into the properties of the object 
    
    in the bucket to scrap the title, name, and link.
    """
    for item_data in data:
        # I couldn't access to the information by indexing nor
        # properties, so I converted the data in a dictionary.
        item_data = item_data.__dict__

        item = SubElement(parent_element, 'item')

        title = SubElement(item, 'title')
        title.text = item_data['name']

        link = SubElement(item, 'link')
        link.text = item_data['_properties']['selfLink']

        description = SubElement(item, 'description')
        description.text = item_data['_properties']['name']

def upload_blob(bucket, content, destination_blob_name):
    """Upload a file into the bucket destination.
    """
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content)


def main(event, context):
    """Connect and access to the bucket,
    
    and write the file.
    """
    bucket = storage_client.get_bucket(bucket_name)
    blobs = storage_client.list_blobs(bucket_name, prefix=folder_name)

    # Return an interator and move to the next position, so avoid the folder name
    files = iter(blobs)
    next(files)

    channel = Element('channel')
    title = SubElement(channel, 'title')
    title.text = "podcasts"
    comment = Comment('Generated for Learning')
    channel.append(comment)
    gather_items(channel, files)
    upload_blob(bucket, prettify(channel), 'rssfeed.xml')
 