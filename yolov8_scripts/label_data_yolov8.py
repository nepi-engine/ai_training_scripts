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
# Update Files and Folders, then Label
##########################################


imports = True
try:
    import os
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

if imports == False:
    sys.exit(1) # Terminate the script with an exit code (e.g., 1 for error)


##########################################
# Methods
##########################################


###############################################
# Main
###############################################

if __name__ == '__main__':
    print('Starting data labeling process')

    if os.path.exists(data) == False:
        print('Failed to find required project folder: ' + data + " " + str(e))
        return

    folders_to_process=get_folder_list(data)
    
      success = fix_folder_permissions(folder)

      success = ai_utils.remove_bad_image_files(folder)
      
