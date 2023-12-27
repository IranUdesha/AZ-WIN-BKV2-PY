import subprocess
import logging #Import Logging Library
from datetime import date, timedelta # Import date class from datetime module
import os
import sys
import re
import psutil
import platform

# Date
today = date.today()

def set_cpu_priority_high(process_id):
    try:
        process = psutil.Process(process_id)

        if platform.system() == "Windows":
            # Set CPU priority on Windows
            process.nice(psutil.HIGH_PRIORITY_CLASS)
            
            print(f"Process {process_id} priority set to high on Windows.")
            logging.info(f"Process {process_id} priority set to high on Windows.")
            # print(f"Memory infor - {process.memory_info()}")
            # print(f'CPU Percent - {process.cpu_percent()}')
            # print(f'CPU Times - {process.cpu_times()}')
            # print(f'CPU Affinity - {process.cpu_affinity()}')
            # print(f'CPU Nice - {process.nice()}')
            # print(f'number of threads - {process.num_threads()}')
            # print(f'status - {process.status()}')
                        
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            # Set CPU priority on Linux or macOS
            os.nice(-20)  # -20 is the highest priority, 20 is the lowest
        else:
            print("Unsupported platform for setting CPU priority.")

    except psutil.NoSuchProcess as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


#Compress all
def compress_all(winrar,bk_name,data_file):
    print("\033[96mFile Compression is Started\033[00m")
    result = ''
    #list Folder Contents
    f_containt = os.listdir(data_file)
    #print(f'All the Files in {data_file} - {f_containt}')
    logging.info(f"File Compression is Started")
    
    for file in f_containt:
        file_name = '_'.join(re.findall(r'[A-Za-z]+', file.split('.')[0])) #Remove all the special characters & numbers from the file name
        # print(f'File Name - {file_name}')
        arguments = [winrar,"a",f"{bk_name}-{file_name}.rar",f'{data_file}{file}']
        
        process =subprocess.Popen(arguments, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        pid = process.pid # Get the process ID
        print(f'Process ID - {pid}')
        logging.info(f"Process ID - {pid}")
        
        set_cpu_priority_high(pid) # Set CPU priority to high for the current process
        
        return_status = process.wait() # Wait for the process to finish
        print(f"Return Status: {return_status}")
        logging.info(f"Return Status: {return_status}")
        
        output, error = process.communicate() # Get the output and error (if any)
        
        if return_status != 0:
            logging.error(f'RAR Compression is faild -{data_file}{file}')
            logging.error(f"Error - {error}")
            logging.info(msg=output,exc_info=True)
            print( f'\033[91mstderr: {error} \033[00m' )
            result = 1
            sys.exit() 
        else :
            logging.info(f"{data_file}{file} RAR Compression is Completed")
            # logging.info(msg=process,exc_info=True)
            print(f"\033[92m{data_file}{file} RAR Compression is Completed \033[00m")
            result = 0
    return result


