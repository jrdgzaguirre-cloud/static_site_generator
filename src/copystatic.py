import os
import shutil

def destination_creator(source_path, destination_path): 
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)

    source_to_destination(source_path, destination_path)

def source_to_destination(source_path, destination_path): 
    for item in os.listdir(source_path):
        source_item = os.path.join(source_path, item)
        destination_item = os.path.join(destination_path, item)
        if os.path.isfile(source_item):
            print(source_item)
            shutil.copy(source_item, destination_item)
        if os.path.isdir(source_item):
            print(source_item)
            os.mkdir(destination_item)
            source_to_destination(source_item, destination_item)