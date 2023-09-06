from azure.storage.blob import BlobServiceClient
import os
from django.conf import settings
from app.models import MetaData




# metadata = MetaData.objects.get(key='BLOB')
# connection_string = metadata.value.get('connection_string')
# container = metadata.value.get('container')




def upload_blob(filepath : str):
    metadata = MetaData.objects.get(key='BLOB')
    connection_string = metadata.value.get('connection_string')
    container = metadata.value.get('container')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)    
    container_client = blob_service_client.get_container_client(container=container)
    with open(filepath, "rb") as data:
        container_client.upload_blob(name= os.path.basename(filepath),data=data,overwrite=True) 


        
def download_blob(filename : str):
    metadata = MetaData.objects.get(key='BLOB')
    connection_string = metadata.value.get('connection_string')
    container = metadata.value.get('container')
    remotepath = filename
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)    
    container_client = blob_service_client.get_container_client(container=container)
    downlaod_obj = container_client.download_blob(blob=remotepath)
    data = downlaod_obj.readall()
    save_blob(filename,data)

 
def save_blob(filename : str,file_content):
        try:
            download_file_path = os.path.join(settings.MEDIA_ROOT,"files",filename)
            os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
            with open(download_file_path, "wb") as file:
                file.write(file_content)
            print("File has been downloaded check on path {}".format(download_file_path))    
        except Exception as e :
            print("Below exception occured while downloading{e}".format(e))
            
            
            
            
            
            