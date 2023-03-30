from django.http import HttpResponse
from django.db import connection
from datetime import date


def reset_today_price(request):
    try:
        cursor = connection.cursor()
        # #public.app_dtn_load
        query_costomer_delete = """delete  from public.app_cust_price where date = '{}' """.format(date.today())
        query_location_delete = """delete  from public.app_location_price where date = '{}' """.format(date.today())
        query_dtn_load_delete = """ delete  from public.app_dtn_load where date = '{}' and day_id = 0 """.format(date.today())
        
        # query_costomer_delete = """delete  from app_cust_price where date = "{}" """.format(date.today())
        # query_location_delete = """delete  from app_location_price where date = "{}" """.format(date.today())
        # query_dtn_load_delete = """ delete  from app_dtn_load where date = "{}" and day_id = 0 """.format(date.today())
        
        cursor.execute(query_costomer_delete)
        cursor.execute(query_location_delete)
        cursor.execute(query_dtn_load_delete)
    except Exception as e:
        print(e)
        return HttpResponse ("Error while deleting")    
    else:
        return HttpResponse ("Successfully deleted today prices")
    finally:
        print("check")
    


