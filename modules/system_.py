import shutil  #Import Directory remove Library
import os
import logging #Import Logging Library
import sys
import subprocess

#Delete Old Backup
def delete_directory(backup_location):
    if os.path.exists(backup_location):
        try:
            os.remove(backup_location)
            print(f"\033[92m{backup_location} is deleted...!\033[00m")
            logging.info(f" {backup_location} is deleted...!")
            delete_result = 0
        except OSError as e:
            print("\033[91mError: %s - %s.\033[00m" % (e.filename, e.strerror))
            logging.error("Error: %s - %s." % (e.filename, e.strerror),exc_info=True)   
            delete_result = 1  
    else:
        print(f"\033[91mThere is No file in {backup_location}...!\033[00m")
        logging.warning(f"There is No file in {backup_location}...!")
        delete_result = 1
    return delete_result


def disk_details(disk_path): #Get the Hard disk Usage Details
    total, used, free = shutil.disk_usage(disk_path)

    disk_total = round(total / (1024.0 ** 3), 4)
    disk_usage = round(used / (1024.0 ** 3), 4)
    disk_free_space = round(free / (1024.0 ** 3), 4)
    # print(f"Total: {disk_total} GB" )
    # print(f"Used: {disk_usage} GB" )
    # print(f"Free: {disk_free_space} GB")
    return disk_total, disk_usage, disk_free_space


#Install Dependancies
def deps_install():
    
    deps_install_status = 0
    if os.path.exists(f"logs/dep_log.log"):
        with open(f"logs/dep_log.log", 'r') as f:
            for line in f:
                # Split each line into key-value pairs
                parts = line.strip().split('=')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    deps_install_status = value
    else:
        deps_install_status = 0   
        
    if deps_install_status != "1":
        try:
            result = subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
          
            variables = {"deps_install_status": "1"}

        except:
          print('\033[91mAn exception occurred while installing dependancies...! \033[00m')
          variables = {"deps_install_status": "0"}

        with open(f"logs/dep_log.log", 'w') as file:
            for key, value in variables.items():
                file.write(f"{key} = {value}\n")
    else:
        print(f"\033[93mDependancies are already installed...!\033[00m")
        logging.info(f"Dependancies are already installed...!")
        result = 0
    return result
    
def p_logo(path):
    if os.path.exists(path): #Check whether the file exist 
        file = open(path, "r" ) #Open the file
        lines = file.readlines() #read lines
        for line in lines :
            print(f'\033[92m{line.strip()}\033[00m')

    # #pip install art==5.8
    # from art import * 
    # logo_art = text2art("hSenidBiz" ,font='standard')
    # print(f'\033[92m{logo_art}\033[00m')
    # print(f'\033[92mhSenid Business Solutions PLC Backup Script\033[00m')

    # print("* * * * * * * * * * * * * * * * * * * * * * * * * * * ")
        




