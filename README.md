# Introduction 
This Python Script Contain code for Compress folder contain and Upload it to Azure Storage Account.

</br>This Script will Compress Each file in the *sql* folder and save it in *backups* folder and finnaly upload them into respective Container in azure storage Account and will sent an email 

# Dependencies
</br>Winrar
</br>Need Azure Storage Account with 4 Containers name as 'daily','weekly','monthly','yearly'


# Fill The Following before Run This Script
server_name = "<Server Name>"

smtp_server = "<SMTP Server>"
</br>smtp_port = "<SMTP Port>"
</br>smtp_un = "<SMTP Username>"
</br>smtp_pw = "<SMTP Password>"

connection_string = "<Azure Storage Connection String>"
</br>storage_Account_Name= "<Azure Storage Account Name>"


*CPU priority is set to high for Compression part in the Script