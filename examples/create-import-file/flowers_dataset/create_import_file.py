import os
import json
import random

"""
Program to create input JSON files for single label image classification dataset stored in folders based on labels.
"""

bucket_name = ""
test_train_split_specified = 0

train_split = 0
validation_split = 0
test_split = 0

ml_uses = ["train", "validation", "test"]

json_list = []

folder_names = [name for name in os.listdir(".") if os.path.isdir(name)]

#Specify requirements
bucket_name = input("\nBucket name: ")
test_train_split_specified = 1 if 'y' == input("\nDo you want to use train/validation/test split? ([y]es/[n]o): ") else 0

if test_train_split_specified == 1:
    while train_split <= 0:
        train_split = [int(x) if int(x)>0 and int(x)<=100 else 0 for x in [input("\nTrain split (%): ")]][0]
    if train_split < 100:
        while validation_split <= 0:
            validation_split = [int(x) if int(x)>0 and int(x)<=100-train_split else 0 for x in [input("\nValidation split (%): ")]][0]
    test_split = 100 - (train_split + validation_split)

#Create input JSON file
for class_label in folder_names:

    image_files = [name for name in os.listdir("./{}".format(class_label))]

    for image_file_name in image_files:
        
        json_line = {"imageGcsUri": "gs://{}/{}/{}".format(bucket_name, class_label, image_file_name),
                     "classificationAnnotation": {"displayName": class_label}}

        if test_train_split_specified == 1:
            
            json_line["dataItemResourceLabels"] = {"aiplatform.googleapis.com/ml_use":
                                                   random.choices(ml_uses, weights=(train_split, validation_split, test_split))[0]}
            
        json_list.append(json.dumps(json_line))

with open('image_classification_single_label.jsonl', 'w') as f:
    f.write("\n".join(json_list))
