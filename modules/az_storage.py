#pip install azure-storage-blob azure-identity

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def list_containers(con_string):
    
    # Create a BlobServiceClient object using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(con_string)
    
    # List all containers in the storage account
    containers = blob_service_client.list_containers()
    
    # Print the names of the containers
    for container in containers:
        print(container.name)
    return containers


#list_containers(connection_string)

def list_blobs(con_string, container_name):
     # Create a BlobServiceClient object using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(con_string)
    
    container_client = blob_service_client.get_container_client(container=container_name)

    blob_list = container_client.list_blobs()

    for blob in blob_list:
        print(f"Name: {blob.name}")
        
#list_blobs(connection_string,"weekly-backup")

def upload_blobs(con_string,con_name,blob_name,file_path):
    # Create a BlobServiceClient object using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(con_string)
    container_client = blob_service_client.get_container_client(con_name)
    blob_client = container_client.get_blob_client(blob_name)

    print("\033[96mFile Upload is Started\033[00m")
    with open(file_path, "rb") as stream:
        return blob_client.upload_blob(stream,overwrite=True)


#a=upload_blobs(con_string=connection_string, con_name="weekly-backup",blob_name="Test-name-001.txt",file_path="requirements.txt")
#print(a)
