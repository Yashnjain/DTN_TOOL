from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from datetime import date,timedelta
from app.models import dtn_load

def authorisation(func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(id=1).exists():
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to access this page.")
    return wrapper


def setdate(id:int):
    try :
        if id == 0:
            return (date.today(),date.today() - timedelta(days=1))
        elif id == 1:
            return (date.today() - timedelta(days=1),date.today() - timedelta(days=2))
        else :
            return False
    except Exception as e:
        raise Exception (e)    
            
        
def dtn_load_update(id):
    if id == 0:
        maxstatus = None
        try:
            maxstatus = dtn_load.objects.filter(date= date.today(),day_id = 0).values("loadno").order_by("-loadno").first()["loadno"]
        except:
            maxstatus = False
        if maxstatus:
            maxstatus = maxstatus + 1
        else:
            maxstatus = 1    
                
        dtnload = dtn_load(loadno = maxstatus,date = date.today())  
        dtnload.save()   
    else:
        maxstatus = None
        try:
            maxstatus = dtn_load.objects.filter(date= date.today(),day_id = 1).values("loadno").order_by("-loadno").first()["loadno"]
        except:
            maxstatus = False
        if maxstatus:
            maxstatus = maxstatus + 1
        else:
            maxstatus = 1    
                
        dtnload = dtn_load(loadno = maxstatus,date = date.today(),day_id = 1)  
        dtnload.save()
            
        
def get_location_mapping(mapping_list,location):
    filtered_mapping = []
    for mapping in mapping_list:
            if mapping["location_id"] == int(location):
                filtered_mapping.append(mapping)
    return filtered_mapping
        
        
        
def cust_exits_on_date(cust_list,date,ctpm):
    for cust in cust_list:
        if cust["date"] == date and cust["cust_term_prod_id"] ==ctpm:
            return True
    return False    


def get_cust_price_by_date(cust_list,date,ctpm):
    for cust in cust_list:
        if cust["cust_term_prod_id"] ==ctpm:
            return cust["price_variance"]
    return 0   


def get_prev_location_date(locations_price,date):
    for location_price in locations_price:
        if location_price["date"] < date:
            return location_price["date"]
        


def get_location_price_by_date(location_list,date):
    filtered_location = []
    for location in location_list:
        if location["date"] == date:
            filtered_location.append(location)
    return filtered_location             


def get_location_price_id_by_date(location_list,date):
    filtered_location = {}
    for location in location_list:
        if location["date"] == date:
            filtered_location[location["location_id"]] = location["price_dffernce"]
    return filtered_location 

def get_price_at_location(location_list,date,id):
    for location in location_list:
        if location['date'] == date and location["location_id"] == int(id):
            return location["price"]
        
def get_pricediff_at_location(location_list,date,id):
    for location in location_list:
        if location['date'] == date and location["location_id"] == int(id):
            return location["price_dffernce"]        
        

def get_location_dict(location_list,date,id):
    for location in location_list:
         if location['date'] == date and location["location_id"] == int(id):
             return location
    return False     
        
def get_cust_dict(cust_list,id):
    for cust in cust_list:
        if cust["cust_term_prod_id"] == id:
            return cust
    return False        


def get_terminal_dict(tcpmapping_list,ctp_id):
    filter_tcp = []
    for tcp in tcpmapping_list:
        if tcp['id'] == ctp_id and tcp["status"] ==True and tcp['customer__send_format'] == 0:
            filter_tcp.append(tcp)
    return filter_tcp


def get_terminal_mail_dict(tcpmapping_list,ctp_id):
    filter_tcp = []
    for tcp in tcpmapping_list:
        if tcp['id'] == ctp_id and tcp["status"] ==True and tcp['customer__send_format'] == 1:
            filter_tcp.append(tcp)
    return filter_tcp




def get_location_list(location_list,date,id):
    filter_location = []
    for location in location_list:
         if location['date'] == date and location["location_id"] == int(id):
             filter_location.append(location)
    return filter_location


def dtn_filter_last_updated(cust_price_all,for_date,tcpmapping_all,dtn_load_status = 0):
    filterd_list = []
    final = []
    for cust_price in cust_price_all:
        if cust_price['date'] == for_date and cust_price['status'] == dtn_load_status:
            filterd_list = filterd_list + dtn_filter_mapping(tcpmapping_all,cust_price["cust_term_prod_id"],filterd_list)
    for cust_price in cust_price_all:
        if cust_price["cust_term_prod_id"] in filterd_list and cust_price["date"] == for_date:     
            final.append(cust_price)
    return final
            
    
    
            

def dtn_filter_mapping(tcpmapping_all,cid,filterd_list):
    
    for tcp in tcpmapping_all:
        if tcp['id'] == cid:
            if tcp["id"] in filterd_list:
                return [] 
            filter_cust = dtn_filter_customer(tcpmapping_all,tcp["customer_id"])
            return filter_cust
            

            
def dtn_filter_customer(tcpmapping_all,cust_id):
    filter_cust = []
    for tcp in tcpmapping_all:
        if tcp["customer_id"] == cust_id:
            filter_cust.append(tcp["id"])
    return  filter_cust






def dtn_load_all_cust_price(cps_all,for_date):
    filter = []
    for cps in cps_all:
        if cps['date'] == for_date:
            filter.append(cps)
    return filter
    
    
    
def get_today_cust_price(cust_all,date):
    filter = {}
    for cust in cust_all:
        if cust['date'] == date:
            filter[cust["cust_term_prod_id"]]  = cust
    return filter

def get_today_cust_price_dict(cust_all,date):
    filter_dict = {}
    for cust in cust_all:
        if cust['date'] == date:
            # filter_dict[cust["cust_term_prod_id"]] = cust["price_variance"]
            filter_dict[cust["cust_term_prod_id"]] = cust
    return filter_dict       


def strformat(string : str) -> str:
    # return "'{}'".format(s)
    return '\"{}\"'.format(string)