import os
import json
import random

"""
Program to create input JSON files for single label image classification dataset stored in folders based on label.
"""

bucket_name = ""
test_train_split_specified = 0

train_split = 0
test_split = 0
validation_split = 0

ml_uses = ["train", "test", "validation"]

json_list = []

folder_names = [name for name in os.listdir(".") if os.path.isdir(name)]

#Specify requirements
bucket_name = input("\nBucket name: ")
test_train_split_specified = 1 if 'y' == input("\nDo you want to use train/test/validation split? ([y]es/[n]o): ") else 0

if test_train_split_specified == 1:
    while train_split <= 0:
        train_split = [int(x) if int(x)>0 and int(x)<=100 else 0 for x in [input("\nTrain split (%): ")]][0]
    if train_split < 100:
        while test_split <= 0:
            test_split = [int(x) if int(x)>0 and int(x)<=100-train_split else 0 for x in [input("\nTest split (%): ")]][0]
    validation_split = 100 - (train_split + test_split)

#Create input JSON file
for class_label in folder_names:

    image_files = [name for name in os.listdir("./{}".format(class_label))]

    for image_file_name in image_files:
        
        json_line = {"imageGcsUri": "gs://bucket/{}".format(bucket_name+"/"+class_label+"/"+image_file_name),
                     "classificationAnnotation": {"displayName": class_label}}

        if test_train_split_specified == 1:
            
            json_line["dataItemResourceLabels"] = {"aiplatform.googleapis.com/ml_use":
                                                   random.choices(ml_uses, weights=(train_split, test_split, validation_split))[0]}
            
        json_list.append(json_line)

with open('image_classification_single_label.jsonl', 'w') as f:
    json.dump(json_list, f)
