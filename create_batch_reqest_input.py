import os
import json
import random
import imghdr

"""
Program to create JSON input files for batch prediction for images stored in a folder.
"""

bucket_name = ""

json_list = []

#Input bucket name and name of the folder containing the batch
batch_path = input("\nURI of the batch directory (starting with the bucket name, e.g: bucket/batch): ")
folder_name = input("\nName of the local folder containing the batch (must be in the same directory as the python file): ")

#Create input JSON file
image_files = [name for name in os.listdir("./{}".format(folder_name))]

for image_file_name in image_files:

    image_type = imghdr.what('./{}/{}'.format(folder_name, image_file_name))
    json_line = {"content": "gs://{}/{}".format(batch_path, image_file_name), "mimeType": "image/{}".format(image_type)}
    json_list.append(json.dumps(json_line))

with open('image_classification_batch.jsonl', 'w') as f:
    f.write("\n".join(json_list))
