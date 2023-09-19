from django.db import connection
import pandas as pd
import json     
import requests
from datetime import datetime,timedelta
from django.http import HttpResponse
from app.models import MetaData
from .utils import validate_user
from app.models import MetaData



def format_records(df:pd.DataFrame)->json:
    try:
        df['U_Time'] = '0001'
        df.columns = ['U_Date', 'U_WhsCode', 'U_CustCode', 'U_CustName', 'U_Price', 'U_Time']
        df['U_Date'] = df['U_Date'].apply(lambda x : str(x)) 
        filtered_df = df[['U_WhsCode','U_CustCode','U_CustName','U_Price','U_Time']]
        data = {"U_Date" : df.U_Date[0], "DTNP1Collection":filtered_df.to_dict(orient='records')}
        json_data = json.dumps(data)
        return json_data
    except Exception as e :
        raise e     
        
def get_token(metadata : json) ->None:
    try:
        
        login_url = metadata.value.get('tokenurl')
        payload = json.dumps({"UserName": metadata.value.get('username'),"Password": metadata.value.get('password'),"CompanyDB": metadata.value.get('companydb')})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", login_url, headers=headers, data=payload, verify=False)
        cookies = response.cookies
        token = cookies['B1SESSION']      
        return token
    except Exception as e:
        raise e 
        
def post_data(metadata :json,token : str,json_data :json) ->requests.Response:
    try: 
        data_url = metadata.value.get('posturl')
        headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json','Cookie': f'B1SESSION={token}; ROUTEID=.node4'}
        response = requests.request("POST", data_url, headers=headers, data=json_data,verify =False)
        return response   
    except Exception as e :
        raise e 
        


@validate_user
def push_to_sap(requests):
    try:
        metadata_sql = MetaData.objects.get(key='sap_query')
        sql = metadata_sql.value.get('sql')
        metadata = MetaData.objects.get(key='SAP')
        
        df =  pd.read_sql_query(sql,connection)
        df.u_date =  df.u_date[0] + timedelta(days = 1)
        current_date = datetime.now().strftime("%A")
        json_data = format_records(df)
        token = get_token(metadata)
        response = post_data(metadata=metadata,token=token,json_data=json_data)
        return HttpResponse (response.status_code)
    except Exception as e:
        raise e

