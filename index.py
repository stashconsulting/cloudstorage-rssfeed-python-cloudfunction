from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
# Import gcloud
from google.cloud import storage

# Enable Storage
storage_client = storage.Client()

# Reference an existing bucket.
#bucket = client.get_bucket('image-food-files')
bucket_name = 'image-food-files'
folder_name = 'food/'
blobs = storage_client.list_blobs(bucket_name, prefix=folder_name)
files = iter(blobs)
next(files)

print('ejecuto!')

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def gather_items(parent_element, data):
    for item_data in data:
        item_data = item_data.__dict__
        item = SubElement(parent_element, 'item')

        title = SubElement(item, 'title')
        title.text = item_data['name']

        link = SubElement(item, 'link')
        link.text = item_data['_properties']['mediaLink']

        description = SubElement(item, 'description')
        description.text = item_data['_properties']['name']

# Top elements
channel = Element('channel')
title = SubElement(channel, 'title')
title.text = "podcasts"
comment = Comment('Generated for Learning')
channel.append(comment)
gather_items(channel, files)

with open("rssfeed.xml", "w") as outF:
    outF.write(prettify(channel))
