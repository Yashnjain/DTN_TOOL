import ftputil
from datetime import datetime
import pytz
from app.models import MetaData


def transfer_files(local_file_path):
    try:
        metadata = MetaData.objects.get(key='DTN')
        hostname = metadata.value.get('hostname')
        username = metadata.value.get('username')
        password = metadata.value.get('password')
        with ftputil.FTPHost(hostname,username,password) as ftp_host:
            timezone = pytz.timezone('US/Central')
            date = datetime.now(timezone).strftime("%d%m%Y%H%M")
            file_path = 'TBiourja_' + date[:10] + '.csv'
            ftp_host.upload(local_file_path, file_path)
            print(f"File uploaded: {local_file_path} -> {file_path}")
    except Exception as e:
        raise (f"Error {e} in Loading file to FTP server")

