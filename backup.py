#! /usr/bin/python 
###################################################################################           
# This python script is used for compress sql backup & upload to Azure Storage    #             
# Written by : Iran Udesha                                                        #
# Created date: 14-03-2023                                                        #
# Last modified: 02-11-2023                                                       #
# Tested with : Python 3.11                                                       #
###################################################################################
from datetime import date, timedelta # Import date class from datetime module
import logging #Import Logging Library
import os
os.system('color FF') #Enable Colours on CMD

# Date
today = date.today()
yesterday =  today - timedelta(days=1)
weekly_backup_day ="Friday"

import modules.system_ as system
#Print Logo
system.p_logo("templates/logo.txt")

server_name = "<Server Name>"

#Logging Details
logging.basicConfig(handlers=[logging.FileHandler(filename=f"logs/{server_name}-Backup-{today.strftime('%d-%m-%Y')}.txt", 
                                                 encoding='utf-8', mode='a+')],
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.DEBUG)
# Creating log file
logger = logging.getLogger()


#Install Dependancies
system.deps_install()


from modules import fsize, frar
import modules.az_storage as az_storage
import modules.email_conf as email_conf 
import codecs#Library for open HTML templates and replace values
from jinja2 import Template #Library for generate HTML templates

html_content_file= "templates/html-content.html" #Original HTML Template
html_template = "templates/html-notification.html" #Updated HTML Template Location

#html_file=codecs.open(html_template, 'r', "utf-8")

# SMTP Details
smtp_server = "<SMTP Server>"
smtp_port = "<SMTP Port>"
smtp_un = "<SMTP Username>"
smtp_pw = "<SMTP Password>"

receivers= ['<Email Address>']

#Dependancies
winrar = "C:/Program Files/WinRAR/Rar.exe"
sql_location = "sql/"
rar_save_location = "backups/"

backup_name = f'{rar_save_location}{server_name}'

#Cloud Storage Details
container_list = ["daily"]

if(today.day == 1):
    container_list.append("monthly")
    
if(today.strftime("%A") == weekly_backup_day):
    container_list.append("weekly")

if(today.month == 1 and today.day == 1):
    container_list.append("yearly")

# Set your Azure Storage account connection string
connection_string = "<Azure Storage Connection String>"
storage_Account_Name= "<Azure Storage Account Name>"

class db_backup:
    def __init__(self ):
      self.db_name = "Error"
      self.odb_size = "Error"
      #self.availability = False
      #self.odb_status = False
      self.ndb_size = 0
      self.ndb_bk_status = 'Fail'
      self.upload_storage_acc = storage_Account_Name
      self.upload_status = []

dbbackup = db_backup()
db_list = {}

logging.info("")
logging.info(f"****** {server_name}-{today} Daily Backup ******") 

#check yesterday Backup Size
if os.path.exists(f'{rar_save_location}'):
    #list all files in backup folder
    files = os.listdir(rar_save_location)
    print(f'Number of Files in Backups folder - {files.__len__()}' )
    logger.info(f'Number of Files in Backups folder - {files.__len__()}')
    if files.__len__() > 0: 
        
        for file in files:
            if file.endswith(".rar"):
                db = db_backup()
                db.db_name = file.split('.')[0]
                odb_size = fsize.file_size(f'{rar_save_location}{file}')
                db.odb_size = f'{round(odb_size[0],3)} {odb_size[1]}'
                db_list[db.db_name] = db
        
        print(f"\033[93mYesterday backup details\033[00m")
        
        for key in db_list:    
            print(f'\033[96mDB-Name= {db_list[key].db_name}, DB-Size= {db_list[key].odb_size}\033[00m')
            logging.info(f'DB-Name= {db_list[key].db_name}, DB-Size= {db_list[key].odb_size}')  
        
        #keep empty line
        print(" ")
        logging.info(" ")
        
        #Delete Yesterday Backup
        old_backup_status = ''
        for file in files:  
            
            try:
                sys_reply = system.delete_directory(f'{rar_save_location}{file}')
                if sys_reply == 0:
                    old_backup_status = "Deleted"
            except:
                print('An exception occurred')
                old_backup_status = "Unable to Delete"
         
    else:
        print(f"\033[91mThere is no Yesterday backup in {rar_save_location}\033[00m")
        logging.info(f"There is no Yesterday backup in {rar_save_location}")                 
        
#Compress SQL Files
rar_reply = frar.compress_all(winrar=winrar,bk_name=backup_name,data_file = sql_location)
#print(rar_reply)

if rar_reply == 0 :
    #check New Backup Datails    
    new_files = os.listdir(rar_save_location)
    print(f'Number of new backups in Backups folder - {new_files.__len__()}' )

    if db_list.__len__() == 0 and new_files.__len__() > 0: # No Yesterday Backup and New Backup is available

        #add new DB Backups details to DB List
        for file in new_files:
            if file.endswith(".rar"):
                ndb = db_backup()
                ndb.db_name = file.split('.')[0]
                ndb_size = fsize.file_size(f'{rar_save_location}{file}')
                ndb.ndb_size = f'{round(ndb_size[0],3)} {ndb_size[1]}'
                db_list[ndb.db_name] = ndb
    elif db_list.__len__() > 0 and new_files.__len__() > 0: # Yesterday Backup and New Backup is available
        #add new DB Backups details to DB List
        for file in new_files:
            if file.endswith(".rar"):
                if file.split('.')[0] in db_list: #check new backup name is already in DB List
                    ndb_size= fsize.file_size(f'{rar_save_location}{file}')
                    db_list[file.split('.')[0]].ndb_size = f'{round(ndb_size[0],3)} {ndb_size[1]}'
                    
                else: #add new backup name to DB List
                    ndb = db_backup()
                    ndb.db_name = file.split('.')[0]
                    ndb_size = fsize.file_size(f'{rar_save_location}{file}')
                    ndb.ndb_size = f'{round(ndb_size[0],3)} {ndb_size[1]}'
                    db_list[ndb.db_name] = ndb
                    

    #Upload 
    for container in container_list:
    #Upload Data into Azure Storage
        for key in db_list:

            try:
                resp = az_storage.upload_blobs(con_string=connection_string,con_name=container,blob_name=f'{server_name}/{today}/{db_list[key].db_name}.rar',file_path=f'{rar_save_location}{db_list[key].db_name}.rar')
                print(f"\033[92m{rar_save_location}{db_list[key].db_name}.rar File Upload is Completed \033[00m")  
                logger.info("Upload is Completed")
                up_date = resp['last_modified']
                up_etag = resp['etag'] 
            
            except:
                logger.error(f"Error - Upload is Failed")
                # logger.error(resp)
                print('\033[91mException occurred - Upload is Failed\033[00m')
                up_date = "Upload is Failed"
                up_etag = "Error"
            finally:
                # print(f"Etag - {up_etag}, Upload Date: {up_date}")
                db_list[key].upload_status=(f"Etag - {up_etag}, Upload Date: {up_date}")

else:
    print(f'\033[91mFile Compression is failed..! \033[00m')
    #new_bk.size = "Error"  
    exit
    
#get Current Disk status
total,Usage,free_space= system.disk_details("./")
disk_letter = os.getcwd().split(':')[0]

# convert db_list to list of dictionaries
db_list = [vars(db_list[key]) for key in db_list]

# Load the HTML template Content 
with open(html_content_file) as template_file:
    template = Template(template_file.read())

# Render the template with the data
html_content = template.render(data=db_list)

# Save the HTML content to the output file
with open(html_template, 'w') as file:
    file.write(html_content)


# #Send Email Notifications
for index_num in range(len(container_list)):
    html_file=codecs.open(html_template, 'r', "utf-8")
    html_updated = html_file.read().format(date = today, system = server_name,disk_drive=disk_letter,free_space=free_space,used_space=Usage )

    for receiver in receivers:
        print(receiver)
        email_conf.send_email(sender_email=f"{server_name}@hsenidbiz.com", receiver_email=receiver, 
                        subject=f"{server_name} {today} {container_list[index_num]} Backup Report", html_template=html_updated,
                        smtp_server=smtp_server,smtp_port=smtp_port,smtp_un=smtp_un,smtp_pw=smtp_pw)
        
        print(f"\033[92mEmail is sent to {receiver}\033[00m")
        logging.info(f"Email is sent to {receiver}")

# for x in new_bk.upload_status:
#     print(x)


                    
# for key in db_list:    
#     print(f'Key {key}')
#     print(f'\033[96mDB-Name= {db_list[key].db_name}, DB-Size= {db_list[key].ndb_size}, Old_size ={db_list[key].odb_size}, Upload - {db_list[key].upload_storage_acc},up Status - {db_list[key].upload_status} \033[00m')  

