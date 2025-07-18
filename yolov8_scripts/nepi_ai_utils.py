#!/usr/bin/env python
#
# Copyright (c) 2024 Numurus, LLC <https://www.numurus.com>.
#
# This file is part of nepi-engine
# (see https://github.com/nepi-engine).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#


############################
# Utility functions for ai training scripts
############################

imports = True
try:
    import os
    import sys
    sys.tracebacklimit = None
    import subprocess
    import glob
    import fileinput
    import random
    import yaml
    import shutil

    import glob
    import fileinput
    import random

    import logging
    import declxml as xml


    from PIL import Image
except Exception as e:
    print("Missing required python modules " + str(e))
    imports = False

    




##########################################
# PORJECT SETTINGS - Edit as Necessary
##########################################
FRAMEWORK_NAME = 'yoloV8'
TYPE_NAME = 'detection'

PROJECT_FILE = 'project_settings.yaml'

DATA_LABEL_FOLDER = 'data_labeling'
MODEL_TRAIN_FOLDER = 'model_training'
MODEL_DEPLOY_FODLER = 'model_deploy'

IMAGE_FILE_TYPES = ['jpg','JPG','jpeg','png','PNG']

CLASSES_FILE_NAME = 'classes.txt'

TRAIN_FILE_NAME = 'data_custom.yaml'

MAX_NUM_IMAGES = -1 #100 # set to -1 to use all
VAL_DATA_PERCENTAGE = 10
TEST_DATA_PERCENTAGE = 10
MAKE_TRAIN_TEST_UNIQUE = True

##########################################
# System Variables
##########################################




# Gather current folder information
abs_path = os.path.realpath(__file__)
current_folder = os.path.dirname(abs_path)
project_folder = os.path.dirname(current_folder)
mount_folder = os.path.dirname(project_folder)

data_folder = os.path.join(current_folder,DATA_LABEL_FOLDER)
model_folder = os.path.join(current_folder,MODEL_TRAIN_FOLDER)
deploy_folder = os.path.join(current_folder,MODEL_DEPLOY_FOLDER)

classes_file = os.path.join(data_folder,CLASSES_FILE_NAME)

train_file = os.path.join(train,TRAIN_FILE_NAME)

img_types = IMAGE_FILE_TYPES

# Read in project settings
project_file = os.path.join(current_folder,PROJECT_FILE)
project_dict = read_yaml_2_dict(file_path):

# Gather owner and group details for project mountpoint
os.stat(mount_folder)
storage_uid = stat_info.st_uid
storage_gid = stat_info.st_gid

##########################################
# Methods
##########################################


def fix_folder_permissions(folder_path):
    print("Checking folder permissions: " + folder_path)
    if os.path.exists(folder_path) == True:
        try:
            os.system('chown -R ' + str(self.storage_uid) + ':' + str(self.storage_gid) + ' ' + folder_path) # Use os.system instead of os.chown to have a recursive option
            #os.chown(full_path_subdir, self.storage_uid, self.storage_gid)
            os.system('chmod -R 0775 ' + folder_path)
        except Exception as e:
            print("Failed to update folder permissions: " + folder_path + " " + str(e))
    return success


def get_folder_list(folder_path):
  filelist=os.listdir(folder_path + '/')
  folder_list=[]
  #print('')
  #print('Files and Folders in Path:')
  #print(folder_path)
  #print(filelist)
  for file in enumerate(filelist):
    foldername = (folder_path + '/' + file[1])
    #print('Checking file: ')
    #print(foldername)
    if os.path.isdir(foldername): # file is a folder
       folder_list.append(foldername)
  return folder_list

def open_new_file(file_path):
  print('')
  if os.path.isfile(file_path):
    print('Deleting existing file:')
    print(file_path)
    os.remove(file_path)
  print('Creating new file: ' + file_path)
  fnew = open(file_path, 'w')
  return fnew

def read_list_from_file(file_path):
    lines = []
    with open(file_path) as f:
        lines = [line.rstrip() for line in f] 
    return lines

def write_list_to_file(data_list, file_path):
    success = True
    try:
        with open(file_path, 'w') as file:
            for data in data_list:
                file.write(data + '\n')
    except Exception as e:
        print("Failed to write list to file " + file_path + " " + str(e))
        success = False
    return success



def read_yaml_2_dict(file_path):
    dict_from_file = dict()
    if os.path.exists(file_path):
        try:
            with open(file_path) as f:
                dict_from_file = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print("Failed to get dict from file: " + file_path + " " + str(e))
    else:
        print("Failed to find dict file: " + file_path)
    return dict_from_file


def write_dict_2_yaml(dict_2_save,file_path,defaultFlowStyle=False,sortKeys=False):
    success = False
    try:
        with open(file_path, "w") as f:
            yaml.dump(dict_2_save, stream=f, default_flow_style=defaultFlowStyle, sort_keys=sortKeys)
        success = True
    except Exception as e:
        print("Failed to write dict: "  + " to file: " + file_path + " " + str(e))
    return success


def copy_file(file_path, destination_path):
    print('')
    if os.path.exists(destination_path) == False:
        with open(pt_file_path, 'x') as f:
            pass
    try:
        shutil.copy(file_path, destination_path)
        print("File: " + file_path + " Copied to: " + destination_path)
    except FileNotFoundError:
        print("Error file " + file_path + "not found") 
    except Exception as e:
        print("Excepton: " + str(e))




def prepare_label_files():
    ## Update Data Labeling Folder
    new_classes = classes
    orig_classes = classes
    classes_changed = False
    if os.path.exists(classes_file) == False:
        orig_classes = classes
        write_list_to_file(classes,classes_file)
    else:
        orig_classes = read_list_from_file(classes_file)
        if orig_classes != classes:
            print('Updated classes.txt labels from ' + str(orig_classes) + ' to ' + str(classes))
            write_list_to_file(classes,classes_file)
    
    folders_to_process=get_folder_list(data_folder)
    for folder in folders_to_process:       
        print('Preparing txt label files in: ' + str(folder))
        labels_changed = orig_classes != new_classes
        has_labels = False
        for f in os.listdir(folder):
            if f.endswith(".xml"):  
                if has_labels == False:
                    print('Updating xml label files in folder : ' + str(folder) + ' from ' + str(orig_classes) + ' to ' + str(classes))
                has_labels = True
                xml_file = os.path.join(folder,f)
                if labels_changed == True:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    for ind, o_entry in enumerate(root.findall("object")):
                        label = o_entry.find("name").text
                        if label in orig_classes:
                        ind = orig_classes.fine(label)
                        if ind != -1:
                            o_entry.find("name").text = new_classes[ind]
                        label = o_entry.find("name").text
                        #print(label)
                    tree.write(xml_file)
            if has_labels == True:
                print('Updating txt label files in folder : ' + str(folder))        
                convert_xml_files(data_folder,classes_file)
  return True


def remove_bad_image_files(folder_path):
  print("Checking for bad images in folder: " + folder_path)
  path, dirs, files = next(os.walk(folder_path))
  data_size = len(files)
  ind = 0
  for f in os.listdir(folder_path):
    f_ext = os.path.splitext(f)[1]
    f_ext = f_ext.replace(".","")
    if f_ext in img_types:
      #print('Found image file')
      image_file = (folder_path + '/' + f)
      #print(image_file)
      # Open and verify the image file
      try:
        img = Image.open(image_file) # open the image file
        img.verify()
        #print('Good file')
      except:
        print('')
        print('Found bad image file:')
        print(image_file) # print out the names of corrupt files
        print('Deleting file')
        os.remove(image_file)
        print('Looking for label files')
        label_file = (folder_path + '/' + f.split(f_ext)[0]+'xml')
        #print(label_file)
        if os.path.exists(label_file):
          print('Found xml label file for bad image:')
          print(label_file) # print out the names of corrupt files
          print('Deleting file')
          os.remove(label_file)
        label_file = (folder_path + '/' + f.split(f_ext)[0]+'txt')
        #print(label_file)
        if os.path.exists(label_file):
          print('Found txt label file for bad image:')
          print(label_file) # print out the names of corrupt files
          print('Deleting file')
          os.remove(label_file)
        else:
          print('No label file found for bad image')


def get_best_model(target_weight):
    weight = None
    print('')
    for dirpath, dirnames, files in os.walk('model_training'):
        for f in files:
            if target_weight in f:
                file_path = os.path.join(dirpath, f)
                #print("Found: " + file_path)
                weight = file_path
    return weight




  

def create_train_file(base_model = project_dict.BASE_MODEL):
    ### Create dictionary
    data = {
        'ai_model' : {
            'framework' : {
                'name' : FRAMEWORK_NAME
            },
            'type' : {
                'name' : TYPE_NAME
            },
            'description' : {
                'name' : project_dict.DESCRIPTION
            },
            'weight_file' : {
                'name' : base_model
            },
            'image_size' : {
                'image_width' : {
                    'value' : project_dict.IMAGE_SIZE
                },
                'image_height' : {
                    'value' : project_dict.IMAGE_SIZE
                }
            },
            'classes' : {
                'names' : project_dict.CLASSES
            }
        }
    }
    success = write_dict_2_yaml(data, yaml_file_path)
    # print("Yaml created: " + success)
    return success




def convert_xml_files(folder_path,classes_file_path):
  transformer = Xml2TxtConverter(folder_path, classes_file_path)
  transformer.transform()

##########################################
# XML Label to TXT File Converter
##########################################

class Xml2TxtConverter(object):
    def __init__(self, folder_path, classes_file):
        self.xml_dir = folder_path
        self.out_dir = folder_path
        self.classes = reader.get_classes(classes_file)


    def transform(self):
        reader = Reader(xml_dir=self.xml_dir)
        xml_files = reader.get_xml_files()
        #print(xml_files)
        classes = self.classes
        #print(classes)
        object_mapper = ObjectMapper()
        annotations = object_mapper.bind_files(xml_files, xml_dir=self.xml_dir)
        self.write_to_txt(annotations, classes)

    def write_to_txt(self, annotations, classes):
        for annotation in annotations:
            output_path = os.path.join(self.out_dir, self.filename_format(annotation.filename))
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            if os.path.exists(output_path) == True:
                os.remove(output_path)
            with open(output_path, "w+") as f:
                f.write(self.convert_2_txt(annotation, classes))

    def convert_2_txt(self, annotation, classes):
        result = []
        for obj in annotation.objects:
            if obj.name not in classes:
                print("Please, add '%s' to classes.txt file." % obj.name)
                exit()
            x, y, width, height = self.get_object_params(obj, annotation.size)
            result.append("%d %.6f %.6f %.6f %.6f" % (classes[obj.name], x, y, width, height))
        return "\n".join(result)

    @staticmethod
    def get_object_params(obj, size):
        image_width = 1.0 * size.width
        image_height = 1.0 * size.height

        box = obj.box
        absolute_x = box.xmin + 0.5 * (box.xmax - box.xmin)
        absolute_y = box.ymin + 0.5 * (box.ymax - box.ymin)

        absolute_width = box.xmax - box.xmin
        absolute_height = box.ymax - box.ymin

        x = absolute_x / image_width
        y = absolute_y / image_height
        width = absolute_width / image_width
        height = absolute_height / image_height

        return x, y, width, height

    @staticmethod
    def filename_format(filename):
        pre, ext = os.path.splitext(filename)
        return "%s.txt" % pre


class Reader(object):
    def __init__(self, xml_dir):
        self.xml_dir = xml_dir

    def get_xml_files(self):
        xml_filenames = []
        for root, subdirectories, files in os.walk(self.xml_dir):
            for filename in files:
                if filename.endswith(".xml"):
                    file_path = os.path.join(root, filename)
                    file_path = os.path.relpath(file_path, start=self.xml_dir)
                    xml_filenames.append(file_path)    
        return xml_filenames

    @staticmethod
    def get_classes(filename):
        with open(os.path.join(os.path.dirname(os.path.realpath('__file__')), filename), "r", encoding="utf8") as f:
            lines = f.readlines()
            return {value: key for (key, value) in enumerate(list(map(lambda x: x.strip(), lines)))}

import logging
import os
import declxml as xml


class ObjectMapper(object):
    def __init__(self):
        self.processor = xml.user_object("annotation", Annotation, [
            xml.user_object("size", Size, [
                xml.integer("width"),
                xml.integer("height"),
            ]),
            xml.array(
                xml.user_object("object", Object, [
                    xml.string("name"),
                    xml.user_object("bndbox", Box, [
                        xml.integer("xmin"),
                        xml.integer("ymin"),
                        xml.integer("xmax"),
                        xml.integer("ymax"),
                    ], alias="box")
                ]),
                alias="objects"
            ),
            xml.string("filename")
        ])

    def bind(self, xml_file_path, xml_dir):
        ann = xml.parse_from_file(self.processor, xml_file_path=os.path.join(xml_dir, xml_file_path))
        ann.filename = xml_file_path
        return ann

    def bind_files(self, xml_file_paths, xml_dir):
        result = []
        for xml_file_path in xml_file_paths:
            try:
                result.append(self.bind(xml_file_path=xml_file_path, xml_dir=xml_dir))
            except Exception as e:
                logging.error("%s", e.args)
        return result


class Annotation(object):
    def __init__(self):
        self.size = None
        self.objects = None
        self.filename = None

    def __repr__(self):
        return "Annotation(size={}, object={}, filename={})".format(self.size, self.objects, self.filename)


class Size(object):
    def __init__(self):
        self.width = None
        self.height = None

    def __repr__(self):
        return "Size(width={}, height={})".format(self.width, self.height)


class Object(object):
    def __init__(self):
        self.name = None
        self.box = None

    def __repr__(self):
        return "Object(name={}, box={})".format(self.name, self.box)


class Box(object):
    def __init__(self):
        self.xmin = None
        self.ymin = None
        self.xmax = None
        self.ymax = None

    def __repr__(self):
        return "Box(xmin={}, ymin={}, xmax={}, ymax={})".format(self.xmin, self.ymin, self.xmax, self.ymax)
