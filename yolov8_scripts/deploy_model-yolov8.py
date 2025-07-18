#!/usr/bin/env python
#
# Copyright (c) 2024 Numurus, LLC <https://www.numurus.com>.
#
# This file is part of nepi-engine
# (see https://github.com/nepi-engine).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#


##########################################
# Copy best.pt and create yaml file
##########################################


imports = True
try:
    import os
    from ultralytics import YOLO
except Exception as e:
    print("Missing required python modules " + str(e))
    print("Connect to internet and run the following in this folder")
    print("sudo pip install -r requirements.txt")
    print("Then try rerunning this script agian")
    imports = False

if imports == True:
  import nepi_ai_utils as ai_utils
  imports = ai_utils.imports
  if imports == True:

    model = ai_utils.project_dict['MODEL_NAME']
    classes = ai_utils.project_dict['CLASSES']
    project = ai_utils.project_folder
    data = ai_utils.data_folder
    train = ai_utils.model_folder
    deploy = ai_utils.deploy_folder
    folders = [data,train,deploy]
    classes_file = ai_utils.classes_file
    train_file = ai_utils.train_file


    start_model = ai_utils.project_dict['BASE_MODEL']
    img_size = ai_utils.project_dict['IMAGE_SIZE']
    num_epochs = ai_utils.project_dict['NUM_EPOCHS']
    batch_size = ai_utils.project_dict['BATCH_SIZE']

if imports == False:
    sys.exit(1) # Terminate the script with an exit code (e.g., 1 for error)




##########################################
# SETUP - Edit as Necessary 
##########################################

data_folder_path = os.path.join(ai_utils.current_folder,'data_labeling')

model_deploy_path = os.path.join(ai_utils.current_folder,'model_deploy')
model_training = os.path.join(ai_utils.current_folder,'model_training')
classes_file_path = os.path.join(data_folder_path,'classes.txt')

pt_file_path = os.path.join(model_deploy_path, train_yolov8_model.model_name + '.pt')
yaml_file_path = os.path.join(model_deploy_path, train_yolov8_model.model_name + '.yaml')

FRAME_WORK_NAME = 'yolov8'
TYPE_NAME = 'detection'
DESCRIPTION_NAME = 'light bulb object detector'


##########################################
# Methods
##########################################




###############################################
# Main
###############################################

if __name__ == '__main__':

    # Get latest weight

    weight_path = get_weight_path("best.pt")

    # Move weight to model_deploy

    if weight_path is not None:
        copy_file_to_new_destination(weight_path, pt_file_path)
    else:
        print("Weight path is None")

    # Create yaml file in model deploy
    create_yaml_file()

