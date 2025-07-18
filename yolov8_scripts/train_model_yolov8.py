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
# Update Files and Folders, then Train
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
# Methods
##########################################


###############################################
# Main
###############################################


if __name__ == "__main__":

    model_name = model
    print("Starting training for model name: " + model_name)

    print("Preparing Label Files")
    success = ai_utils.prepare_label_files()

    try:
        print("Changing to training folder:", train)
        os.chdir(train)  
        cur_folder = os.getcwd()
    except Exception as e:
        print("Error: The specified training folder was not found: " + str(e))

    model_start = None
    if use_last_model == True:

        if best_model is not None:
            if best_m
            print("starting training using model: " + str(model_start))
    if model start is None:
        model_start = os.path.join(train,start_model)
    
    print("starting training with base model: " + str(model_start))
    if cur_folder == train:
        model = YOLO(model_start)
        results = model.train(data=train_file, epochs=num_epochs, imgsz=img_size, batch=batch_size, name=model_name)
