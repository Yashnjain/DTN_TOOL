
from django.shortcuts import render,redirect,reverse
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound,FileResponse,Http404
from django.views import View
from app.models import Terminal, Customer, Product, Terminal_customer_mapping,Location_price,Cust_price,dtn_load,MyFile
# Create your views here.
from  datetime import date 
from datetime import timedelta
from datetime import datetime
import pandas as pd
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.db import transaction
import csv
from django.core.exceptions import PermissionDenied,ValidationError
from django.contrib.auth.models import User,Group,GroupManager
from django.core.mail import send_mail
from app.mail import mail_send,location_price_mail
from app.utils import *
import logging
import time
import os
from django.conf import settings
import concurrent.futures
# # from django_bulk_load import bulk_insert_models
# # from django_bulk_load import bulk_update_models
# import threading
# import itertools




@login_required(login_url="/accounts/microsoft/login")
@authorisation
def home(request,id = 0):
    start_time = time.time()
    try:
        if id not in [0,1]:
            return HttpResponseBadRequest
        #Getting dates base on id
        
        dates = setdate(id)
        if dates:
            today,yesterday = dates
        else:
            return HttpResponseNotFound
        
        # To Track the active page and lastdtn load
      
        if id == 1:
            color = False
            try:
                maxstatus = dtn_load.objects.filter(date= date.today(),day_id = 1).values("loadno").order_by("-loadno").first()["loadno"]
            except:
                maxstatus = False    
            if maxstatus:
                pass
            else:
                try:
                    maxstatus_yesterday = dtn_load.objects.filter(date= today,day_id = 0).values("loadno").order_by("-loadno").first()["loadno"]
                except:
                    maxstatus_yesterday = 1
                if maxstatus_yesterday:
                    dtnload = dtn_load(date = date.today(),loadno = maxstatus_yesterday,day_id = 1)
                    dtnload.save()
                    maxstatus = maxstatus_yesterday  
                else:    
                    maxstatus = False
        else:
            color = True
            try:
                maxstatus = dtn_load.objects.filter(date= today,day_id = 0).values("loadno").order_by("-loadno").first()["loadno"]
            except:
                maxstatus = False       
          
        if id ==0:
            try:
                last_upload_timestamp = MyFile.objects.filter(day_id = 0).order_by("-created_at").first().created_at
            except: 
                last_upload_timestamp = "error loading timestamp"
        else:
            try:
                last_upload_timestamp = MyFile.objects.filter(day_id = 1).order_by("-created_at").first().created_at
            except: 
                last_upload_timestamp = "error loading timestamp"
            
              
        
        # getting the latest dtn upload No,else setting else false for insert case.
        # try:
        #     maxstatus = dtn_load.objects.filter(date= today).values("loadno").order_by("-loadno").first()["loadno"]
        # except:
        #     maxstatus = False
        print(time.time(),"a")
        last_week = date.today() - timedelta(days = 7)
        #query fetching
                
        location_price_all  = list(Location_price.objects.select_related("location").filter(date__gt = last_week).values("id","location_id","date","price","price_dffernce","location__location"))
        cust_price_all = list(Cust_price.objects.filter(date__gt = last_week).values())
        tcpmapping_all  = list(Terminal_customer_mapping.objects.select_related('customer').values("id","Product_id","customer_id","location_id","status","customer__customer"))
        
        
        
        #  Define a function to run the Location Price query
        # def location_price_query():
        #     location_price_all = Location_price.objects.select_related("location").filter(date__gt = last_week).values("id","location_id","date","price","price_dffernce","location__location")
        #     return location_price_all

        #  # Define a function to run the Cust Price query
        # def cust_price_query():
        #     cust_price_all = Cust_price.objects.filter(date__gt = last_week).values()
        #     return cust_price_all

        # # Define a function to run the Terminal Customer Mapping query
        # def tcpmapping_query():
        #     tcpmapping_all = Terminal_customer_mapping.objects.select_related('customer').values("id","Product_id","customer_id","location_id","status","customer__customer")
        #     return tcpmapping_all
        # print(time.time(),"b")
        # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        #     # map each function to the executor and store the results
        #     results = executor.map(lambda f: f(), [location_price_query,cust_price_query,tcpmapping_query])
        # location_price_all,cust_price_all,tcpmapping_all = list(results)
        ##########################################Get#################################################
        # start_date = datetime.now().date() - timedelta(days=5)
        # end_date = datetime.now().date()
        # location_price_all  = Location_price.objects.select_related('location').filter(date_range = [start_date,end_date])
        # cust_price_all = Cust_price.objects.objects.filter(date_range = [start_date,end_date])
        # tcpmapping_all  = Terminal_customer_mapping.objects.select_related('customer')
        
        
            
        
        #sorting datewise
        location_price_all = sorted(location_price_all, key=lambda x: x['date'],reverse =True) 
        print(time.time(),"c")
        if request.method == 'GET':
            logging.info("##########################<Inside GET METHOD>############################")
            #Get t-1 date data based on id
            
            if id == 0:
                # prev_day = location_price_all.filter(date__lt = today).values('date').order_by("-date")[0]['date']
                prev_day = get_prev_location_date(location_price_all,today)
                if prev_day == today:
                    yesterday = location_price_all.values('date').distinct().order_by("-date")[1]['date']
                else:
                    yesterday = prev_day
            elif id == 1:
                #prev_prev_day = location_price_all.filter(date__lt = today).values('date').order_by("-date")[0]['date']
                prev_prev_day = get_prev_location_date(location_price_all,today)
                yesterday = prev_prev_day
                
                   
            #locations_price_yesterday = location_price_all.filter(date = yesterday).values("location__location","date","price","price_dffernce","location")
            locations_price_yesterday = get_location_price_by_date(location_price_all,yesterday)
            
            #Get t date data 
            #locations_price_today = location_price_all.filter(date = today).values("location__location","date","price","price_dffernce","location")
            locations_price_today = get_location_price_by_date(location_price_all,today)
            
            #Yesterday button active deactive
            yesterday_active = True
            day_gap = (today - yesterday).days
            if day_gap > 1:
                yesterday_active = False
            
                 
        
            #Check for T date data 
            submit_active = False
            special_discount_active = False
            if locations_price_today: 
                special_discount_active = True
                #print("Todays data is already there")
                submit_active = True
                if id == 0:
                    try:
                        max_status_customer = Cust_price.objects.filter(date = today).values("status").order_by('-status')[0]['status']
                        dtn_send_max = dtn_load.objects.filter(date = today,day_id = 0).values('loadno').order_by('-loadno')[0]['loadno']
                        if max_status_customer <= dtn_send_max:
                            submit_active = False
                    except:
                        submit_active = True
                else:
                    try:
                        max_status_customer = Cust_price.objects.filter(date = today).values("status").order_by('-status')[0]['status']
                        dtn_send_max = dtn_load.objects.filter(date = date.today(),day_id = 1).values('loadno').order_by('-loadno')[0]['loadno']
                        if max_status_customer <= dtn_send_max:
                            submit_active = False    
                    except:
                        submit_active = True 
            
                
            #Adding Tth date price i.e New price
            # def addtodayprice(location_price_yesterday):
               
            #     #print(location_price_yesterday["location"])
            #     for location_price_today in locations_price_today:
            #         if location_price_today["location"] == location_price_yesterday["location"]:          
            #             return (location_price_today.get("price",0),location_price_today.get("price_dffernce",0))  
            #         # return (0,0)
            print(time.time(),"e")
            location_and_customer = []
            cust_price_today_all_dict = get_today_cust_price_dict(cust_price_all,today)
            cust_price_yesterday_all_dict = get_today_cust_price_dict(cust_price_all,yesterday)
            for location_price_yesterday in locations_price_yesterday:
                # looping through all the location
                # print("working")
                location_result = {}
                location_result["location_name"] = location_price_yesterday["location__location"]
                location_result["yesterday_price"] = round(location_price_yesterday["price"],4)
                # location_result["price_diff"] =  round(location_price_yesterday["price_dffernce"],4)
                location_result["price_diff"] = 0
                
                location_result["location_id"] = str(location_price_yesterday["location_id"])
                if locations_price_today: 
                    
                    # #print(addtodayprice(location_price_yesterday))
                    # check for current date or Tth date data if exits otherwise leave it take only previous day data 
                    try :
                        location_result["new_price"] = get_price_at_location(location_price_all,today,location_result["location_id"])
                        location_result["price_diff"] = get_pricediff_at_location(location_price_all,today,location_result["location_id"])

                    except : 
                        location_result["new_price"],location_result["price_diff"] = (0,0)  
                if location_result["location_id"]:
                    # getting mapping of customer for given location
                    tcpmappings = get_location_mapping(tcpmapping_all,location_result["location_id"])
                    # tcpmappings  = tcpmapping_all.filter(location = 19).values("id","customer__customer","customer_id","status")
                    customer_detail = []
                    #Taking time during intial load
                    
                    for tcp in tcpmappings:
                        # looping through all the mapping         
                        customer_result = {}
                        customer_result["customer_name"] = tcp["customer__customer"]
                        customer_result["status"] = tcp["status"]   
                        ctpm = tcp["id"]
                        customer_result["ctpm"] = str(ctpm)     
                        
                        try:
                            customer_prices_yesterday = 0
                           
                            if locations_price_today: 
                                # if cust_exits_on_date(cust_price_all,today,ctpm):   
                                # if cust_price_all.filter(date = today,cust_term_prod_id = ctpm):
                                    # customer_prices_yesterday = cust_price_all.filter(date = today,cust_term_prod_id = ctpm).values("price_variance")[0]
                                # customer_prices_yesterday = get_cust_price_by_date(cust_price_today_all,ctpm)
                                customer_prices_yesterday_dict = cust_price_today_all_dict.get(ctpm,0)
                                if customer_prices_yesterday_dict:
                                    customer_prices_yesterday = customer_prices_yesterday_dict["price_variance"]
                                    customer_result["base_price"] = customer_prices_yesterday_dict["base_price"]
                                    # base_price = customer_prices_yesterday["base_prices"]
                                else:
                                   customer_prices_yesterday = 0.0
                                   customer_result["base_price"] = location_result["new_price"]
                                    
                                # else:
                                #     # customer_prices_yesterday = cust_price_all.filter(date = yesterday,cust_term_prod_id = ctpm).values("price_variance")[0]  
                                #     # customer_prices_yesterday = get_cust_price_by_date(cust_price_all,yesterday,ctpm)  
                                #     customer_prices_yesterday = 0
                            else:
                                customer_prices_yesterday = cust_price_yesterday_all_dict.get(ctpm,0)
                                if customer_prices_yesterday:
                                    customer_prices_yesterday = customer_prices_yesterday["price_variance"]
                                
                        except:
                            customer_prices_yesterday = 0 
                        # try:
                        customer_result["price_variance"] = customer_prices_yesterday
                       
                        # except:
                        #     customer_result["price_variance"] = 0 
                        customer_detail.append(customer_result)
                       
                    #end intial load    
                    customer_detail = sorted(customer_detail, key=lambda x: x['customer_name'].lower())   
                    location_result["customer"] = customer_detail    
                location_and_customer.append(location_result)
            location_and_customer = sorted(location_and_customer, key=lambda x: x['location_name'].lower()) 
            today_str = str(today)
            yesterday_str = str(yesterday)
            context = {
               "l_y_p" : location_and_customer,
               "active" : color,
               "submit_active" : submit_active,
               "yesterday_active" : yesterday_active,
               "dtnloadsubmit" : maxstatus,
               "yesterday" : yesterday_str,
               "today" : today_str,
               "last_upload_timestamp" : last_upload_timestamp,
               "special_discount_active" : special_discount_active
            }
            end_time = time.time()
            print(time.time(),"f")
            total_time = end_time - start_time
            print(f"Total time taken: {total_time} seconds")
            
            return render (request,"Home9.html",context)
        
        ###########################################Post################################################
        
        elif request.method == 'POST':
            
            if id == 0:
                prev_day = get_prev_location_date(location_price_all,today)
                if prev_day == today:
                    yesterday = location_price_all.values('date').distinct().order_by("-date")[1]['date']
                else:
                    yesterday = prev_day
            elif id == 1:
                prev_prev_day = get_prev_location_date(location_price_all,today)
                yesterday = prev_prev_day        
            
            # Getting post data 
            data = request.POST
            #print(data)
            
            # Dictionary for post data filteration
            location = {}
            price_variance = {}
            cptm = {}
            SP = {}
            
            # Post Data filteration
            for key,value in data.items():
                try:
                    # Location price
                    if key.startswith("L"):
                        location[key[1:]] = float(value) 
                    # Customer price vaiance  
                    elif key.startswith("P"):            
                        price_variance[key[1:]] = float(value) 
                    # Cutomer location mapping    
                    elif key.startswith("C"):         
                        cptm[key[1:]] = value
                    elif key.startswith("SP"):
                        SP[key[2:]] = value
                    else:
                        pass
                except ValueError:
                    raise ValidationError("Enter Valid Data as float or int kindly check if there blank box reload the page and try again",code="500")       
            
            if id == 1:
                try:
                    maxstatus = dtn_load.objects.filter(date= date.today(),day_id = 1).values("loadno").order_by("-loadno").first()["loadno"]
                except:
                    maxstatus = False  
            else:
                try:
                    maxstatus = dtn_load.objects.filter(date= date.today(),day_id = 0).values("loadno").order_by("-loadno").first()["loadno"]
                except:
                    maxstatus = False
            # # query fetching    
            # location_price_all  = Location_price.objects.all()
            # cust_price_all = Cust_price.objects.all()
            # tcpmapping_all  = Terminal_customer_mapping.objects.all()
            
            #list for bulk upload or create
            list_location_insert = []
            list_location_update = []
            list_tcm_update = []
            list_cust_insert = []
            list_cust_update = []
            # if id == 1:
            #     location = get_location_price_id_by_date(location_price_all,today)
            cust_price_today_all = get_today_cust_price(cust_price_all,today)
            for key,value in location.items():
                # location_yesterday_price = location_price_all.filter(date = yesterday,location_id = key).values_list("price")[0][0]      
                location_yesterday_price = get_price_at_location(location_price_all,yesterday,key)
                # locations_price_today = location_price_all.filter(date = today).values("location__location","date","price","price_dffernce","location")
                # if locations_price_today:
                
                # l_price = location_price_all.filter(location_id = key,date = today).first()
                
                l_price = get_location_dict(location_price_all,today,key)
                price_differnece_flag =  False
                if l_price:
                    location_price = round(float(location_yesterday_price) + float(value),4)
                    if l_price["price_dffernce"] != round(float(value),4):
                        price_differnece_flag = True
                        l_price["price_dffernce"] = round(float(value),4)
                        l_price["price"] = round(float(location_yesterday_price) + float(value),4)
                        if l_price["price"] < 0:
                            return HttpResponse ("Currrent Price at location cannot be negative error for location")
                        if maxstatus:
                            l_price["status"] = int(maxstatus) + 1
                        else:
                            l_price["status"] = 0    
                        l_price = Location_price(id = l_price["id"], location_id = int(l_price["location_id"]),date = l_price["date"],price = l_price["price"],price_dffernce = l_price["price_dffernce"],status = l_price["status"])
                        list_location_update.append(l_price)
                        # l_price.save()
                else:
                    location_price = round(float(location_yesterday_price) + float(value),4)
                    if  location_price < 0:
                            return HttpResponse ("Currrent Price at location cannot be negative error for location")
                    l_price = Location_price(location_id = key,date = today,price =round((float(location_yesterday_price) + float(value)),4),price_dffernce = round(float(value),4))
                    # l_price.save()
                    list_location_insert.append(l_price)
                # tcpmappings  = tcpmapping_all.filter(location = key)
                tcpmappings = get_location_mapping(tcpmapping_all,key)
                # #print("###########################################################################################")
                
                for tcp in tcpmappings:
                    if str(tcp["id"]) in list(cptm.keys()):
                        #print("inside tcp")
                        if tcp["status"] == False:
                            tcp["status"] = True
                            # tcp.save()
                            tcps = Terminal_customer_mapping(id = tcp["id"],status = tcp["status"])
                            list_tcm_update.append(tcps)
                    else:
                        if tcp["status"] == True:
                            tcp["status"] = False
                            tcps = Terminal_customer_mapping(id = tcp["id"],status = tcp["status"])
                            list_tcm_update.append(tcps)
                    
                    if str(tcp['id']) in list(price_variance.keys()):
                        
                        #print("insied customer")
                        discount  = float(price_variance[str(tcp['id'])])
                        #print(discount)
                        # cust_price_today = Cust_price.objects.filter(date= date.today())
                        # if cust_price_today:
                        #     #print("today")

                        # customer_price = cust_price_all.filter(date= today,cust_term_prod_id = tcp.id).first()
                        
                        # customer_price = get_cust_dict(cust_price_today_all,tcp['id'])
                        customer_price = cust_price_today_all.get(tcp["id"],False)
                        if customer_price:
                            change = False
                            if customer_price['price_variance'] != round(discount,4):
                                customer_price['price_variance'] = round(discount,4)
                                customer_price['Final_price'] = round((customer_price['base_price'] + customer_price['price_variance'] ),4)
                                if maxstatus:
                                    customer_price['status'] = int(maxstatus) + 1
                                change  = True
                            if str(tcp['id']) in list(SP.keys()):
                                customer_price['base_price'] = float(SP[str(tcp['id'])])
                                customer_price['Final_price'] = round((customer_price['base_price'] + discount),4)
                                if maxstatus:
                                    customer_price['status'] = int(maxstatus) + 1
                                else:
                                    customer_price['status'] = 0
                                change = True    
                            if price_differnece_flag:
                                customer_price['base_price'] = location_price
                            if customer_price['Final_price'] != round((customer_price['base_price'] + discount),4):
                                customer_price['Final_price'] = round((customer_price['base_price'] + discount),4)
                                if maxstatus:
                                    customer_price['status'] = int(maxstatus) + 1
                                else:
                                    customer_price['status'] = 0
                                change = True
                            # if str(tcp['id']) in list(SP.keys()):
                            #     customer_price['base_price'] = float(SP[str(tcp['id'])])
                            #     customer_price['Final_price'] = round((customer_price['base_price'] + discount),4)
                            #     if maxstatus:
                            #         customer_price['status'] = int(maxstatus) + 1
                            #     else:
                            #         customer_price['status'] = 0
                            #     change = True
                                
                            if change:
                            # customer_price.save()
                                customer_price = Cust_price(id = customer_price["id"], cust_term_prod_id = tcp['id'],date =today,price_variance = customer_price['price_variance'],Final_price = customer_price['Final_price'],status = customer_price['status'],base_price = customer_price['base_price'])
                                list_cust_update.append(customer_price)
                        else: 
                            c_p = Cust_price(date= today,price_variance = round(discount,4),Final_price = round((float(location_price) + discount),4),cust_term_prod_id = tcp["id"],base_price = float(location_price))
                            if maxstatus:
                                c_p.status = maxstatus + 1
                            # c_p.save()
                            list_cust_insert.append(c_p)
                # Cust_price.objects.bulk_update(list_cust_update,['price_variance','status','Final_price'])       
                
            end_time = time.time()           
            total_time = end_time - start_time
            print(f"Total time taken: {total_time} seconds")
            #Database upload
            def list_tcm_update_func():
                if list_tcm_update:
                    Terminal_customer_mapping.objects.bulk_update(list_tcm_update,["status"])
            def list_cust_update_func():  
                if  list_cust_update:
                    Cust_price.objects.bulk_update(list_cust_update,['price_variance','status','Final_price','base_price']) 
            def list_location_update_func():      
                if list_location_update:
                    Location_price.objects.bulk_update(list_location_update,['price_dffernce','price','status'])   
            def list_location_insert_func():            
                if list_location_insert:
                    Location_price.objects.bulk_create(list_location_insert)
            def list_cust_insert_func():   
                if list_cust_insert:
                    Cust_price.objects.bulk_create(list_cust_insert)

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(lambda f: f(), [list_tcm_update_func,list_cust_update_func,list_location_update_func,list_location_insert_func,list_cust_insert_func])
            # if list_location_insert:
            #     bulk_insert_models(list_location_insert,list_cust_insert)
            # # if list_cust_insert:  
            # #     bulk_insert_models(list_cust_insert)
            # if list_tcm_update:    
            #     bulk_update_models(models = list_tcm_update,update_field_names = ["status"],pk_field_names = ["id"] )
            # if list_cust_update:
            #     bulk_update_models(models = list_cust_update,update_field_names = ['price_variance','status','Final_price'],pk_field_names = ["id"],)
            # if list_location_update:
            #     bulk_update_models(models = list_location_update,update_field_names = ['price_dffernce','price','status'],pk_field_names = ["id"])
            
            end_time = time.time()           
            total_time = end_time - start_time
            print(f"Total time taken: {total_time} seconds")   
            if id==1:
                return redirect("homeid",1)
            else:
                return redirect("home")
        elif request.method == "PUT":
            pass
    except ValidationError as e:
        return  HttpResponseBadRequest (e)
    except Exception as e:
        #print(e)
        return HttpResponse ("Getting follwing {} error kindly check".format(e))

def strformat(s):
    return '"{}"'.format(s)


    
def genrate_dtn_file(dtnlist : dict,dtncodedict : dict):  
    effective_date = date.today()
    effective_date = effective_date.strftime("%m/%d/%y")
    #print(effective_date)
    f = open("dtn_sample.csv",'w', newline='')
    c = csv.writer(f)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
    c = csv.writer(response)
    data = []
    idpass = ["ABC1","URJA"]
    messagetype  =  ["PRF"]
    commandline = ["CO2","0001"," / / ","00:00","0000","1","0001","S","$"]
    dtncode = ['0008']
    begin = ["BEGIN-BINARY-DATA"]
    header = [strformat('HEADER'),"Customername"]
    detail_item = [strformat("PRICE"),"Terminal","statecode",strformat("MAG"),"Ethanol","product_price","change amount",effective_date,"18:00"]
    note  = [strformat("NOTE"),("FOR QUESTIONS PLEASE CONTACT 012-345-6789, DTN@example.com")]
    end = ["END-BINARY-DATA"]
    c.writerow(idpass)
    c.writerow(messagetype)
    i = 1
    for key,value in dtnlist.items():
        commandline[1] = "000{}".format(i)
        
        c.writerow(commandline)
        dtncode[0] = dtncodedict[key]
        if "," in dtncode[0]:
            dtncode_list = dtncode[0].split(",")
            for i in dtncode_list:
                c.writerow([i])
        else:        
            c.writerow(dtncode)
        c.writerow(begin)
        header[1] = strformat(key)
        c.writerow(header)
        for lp  in value:
            
            detail_item[1] = strformat(lp["location"])
            detail_item[2] = strformat(lp["state"])
            detail_item[5] = format(float(lp["price"]),".4f")
            detail_item[6] = format(float(lp["change"]),".4f")
            if float(detail_item[6]) > 0:
                detail_item[6] = f"+{detail_item[6]}"
            c.writerow(detail_item)
           
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==")
            #print(lp["location"],key)
        c.writerow(note)
        c.writerow(end)
    return response    
    f.close()
        
def download_file(request,id):
    try:
        file_name = MyFile.objects.filter(id =id).values("file").first()["file"]
        file_path = os.path.join(settings.MEDIA_ROOT,"files",file_name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path,"rb"),filename = "dtn.csv")
            return response
        else:
            raise Http404
    except:
        raise Http404
            
    
    
def filter_files(request):
    selected_date = request.GET.get('date')
    if selected_date:
        files = MyFile.objects.filter(created_at__date=datetime.strptime(selected_date, '%Y-%m-%d').date())
    else:
        files = MyFile.objects.all().order_by("-created_at")
    return render(request, 'download.html', {'files': files})


def fetch_dtn_file_data(id,for_date):
    
    today = date.today()
    try:
        
        supplier = {} 
        dtn = {}
        last_week = date.today() - timedelta(days = 7)
        cps_all = Cust_price.objects.filter(date__gt = last_week).values()
        location_price_all  = Location_price.objects.select_related("location").filter(date__gt = last_week).values("id","location_id","date","price","price_dffernce","location__location","location_id__state")
        tcpmapping_all  = Terminal_customer_mapping.objects.select_related('customer').values("id","location_id","status","customer__customer","customer__dtn","customer_id",'customer__send_format')
        if id == 1:
            dtn_load_status = dtn_load.objects.filter(date = today,day_id = 1).order_by("-loadno").values("loadno").first()["loadno"]
            if dtn_load_status:
                cps = dtn_filter_last_updated(cps_all,for_date,tcpmapping_all,(dtn_load_status + 1))
                # cps = Cust_price.objects.filter(date = for_date,status = dtn_load_status + 1).values()
                if cps:
                    pass
                else:
                    return False
                
        else:   
            try:  
                dtn_load_status = dtn_load.objects.filter(date = today,day_id = 0).order_by("-loadno").values("loadno").first()["loadno"] 
            except:
                dtn_load_status = False
                
            if dtn_load_status:
                cps = dtn_filter_last_updated(cps_all,for_date,tcpmapping_all,(dtn_load_status + 1))
                # cps = Cust_price.objects.filter(date = for_date,status = (dtn_load_status + 1) ).values()
            else:     
                cps = dtn_load_all_cust_price(cps_all,for_date)
                
            
        # try:
        #     dtn_load_status = dtn_load.objects.filter(date = for_date).order_by("-loadno").values("loadno").first()["loadno"]
        #   #  dtn_load_status =  dtn_load.objects.filter(date= for_date).values("loadno").order_by("-loadno").first()["load_no"]
        # except:
        #     dtn_load_status = False
        # if dtn_load_status:
        #     cps = Cust_price.objects.filter(date = for_date,status = (dtn_load_status + 1) ).values()
        # else:     
        #     cps = Cust_price.objects.filter(date = for_date).values()
        # last_week = date.today() - timedelta(days = 7)
        # location_price_all  = Location_price.objects.select_related("location").filter(date__gt = last_week).values("id","location_id","date","price","price_dffernce","location__location","location_id__state")
        # # cust_price_all = Cust_price.objects.filter(date__gt = last_week).values()
        # tcpmapping_all  = Terminal_customer_mapping.objects.select_related('customer').values("id","location_id","status","customer__customer","customer__dtn")
        if cps:
            for cp in cps:
                
                # #print((cp["cust_term_prod_id"]))
                if cp:
                    clms = get_terminal_dict(tcpmapping_all,cp["cust_term_prod_id"])
                     #clms = Terminal_customer_mapping.objects.filter(id = cp["cust_term_prod_id"],status = True).values("location_id","customer__customer","customer__dtn")
                    if clms:
                        location_list = []
                        for clm in clms:
                            if clm["customer__customer"] in dtn.keys():
                                pass
                            else:
                                dtn[clm["customer__customer"]] = clm["customer__dtn"]
                            #print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@S')
                            if clm["customer__customer"] in supplier.keys():
                                pass
                            else:
                                supplier[clm["customer__customer"]] = []
                            
                            if clm:
                                lps = get_location_list(location_price_all,for_date,clm["location_id"])
                            #    lps = Location_price.objects.filter(location_id = clm["location_id"],date = for_date).values("price","location_id__location","price_dffernce","location_id__state")
                                if lps:
                                    for lp in lps:
                                        if lp:
                                            #print('check')
                                            loc = dict()
                                            loc["state"] = lp["location_id__state"]
                                            loc["location"] = lp["location__location"]
                                            loc["price"] = cp["Final_price"]
                                            # loc["change"] = lp["price_dffernce"] + cp["price_variance"]
                                            loc["change"] = cp["price_variance"]
                                            # loc["effective_date"] = date.today()
                                            # loc["effective_time"] = "18:00"
                                           
                                            #print("check2")
                                            supplier[clm["customer__customer"]].append(loc) 
        return (supplier,dtn)                                 
    except Exception as e:
        #print("fail")
        return HttpResponse (e) 
    # finally:
    #     #print(supplier)
    #     genrate_dtn_file(supplier,dtn)
   



   
@login_required(login_url="/accounts/microsoft/login")
@authorisation
def load_data_to_dtn(request,id = 0):
    
    for_date = None
    if id == 0:
        for_date = date.today() 
        
    elif id == 1 :
        #print("yesterday")
        for_date = date.today() - timedelta(days=1)
    else:
        return HttpResponseNotFound    
    try:  
        dtnlist,dtncodedict = fetch_dtn_file_data(id,for_date)
        ######################################
        if id == 0:
            effective_date = date.today() + timedelta(days=1)
            effective_date = effective_date.strftime("%m/%d/%y")
        elif id == 1:
            effective_date = date.today()
            effective_date = effective_date.strftime("%m/%d/%y")
        #print(effective_date)
        
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Dtnfile.csv"'},
        )
        c = csv.writer(response)
        data = []
        idpass = ["BUR1","URJA"]
        messagetype  =  ["PRF"]
        commandline = ["CO2","0001"," / / ","00:00","0000","1","0001","S","$"]
        dtncode = ['0008']
        begin = ["BEGIN-BINARY-DATA"]
        header = [strformat("HEADER"),"Customername"]
        detail_item = [strformat("PRICE"),"Terminal","statecode",strformat("MAG"),"Ethanol","product_price","change amount",effective_date,"18:00"]
        note  = [strformat("NOTE"),("FOR QUESTIONS PLEASE CONTACT 012-345-6789, DTN@example.com")]
        end = ["END-BINARY-DATA"]
        c.writerow(idpass)
        c.writerow(messagetype)
        i = 1
        for key,value in dtnlist.items():
            commandline[1] = "000{}".format(i)
            
            c.writerow(commandline)
            dtncode[0] = dtncodedict[key]
            if "," in dtncode[0]:
                dtncode_list = dtncode[0].split(",")
                for i in dtncode_list:
                    c.writerow([i])
            else:        
                c.writerow(dtncode)
            c.writerow(begin)
            header[1] = strformat(key)
            c.writerow(header)
            for lp  in value:
                
                detail_item[1] = strformat(lp["location"])
                detail_item[2] = strformat(lp["state"])
                detail_item[5] = format(float(lp["price"]),".4f")
                detail_item[6] = format(float(lp["change"]),".4f")
                if float(detail_item[6]) > 0:
                    detail_item[6] = f"+{detail_item[6]}"
                c.writerow(detail_item)
            c.writerow(note)
            c.writerow(end)        
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = "{}.csv".format(timestamp)
        file_path = os.path.join(settings.MEDIA_ROOT,"files",filename)
        try:
            with open(file_path, 'w',newline='') as f:
                f.write(response.content.decode('utf-8'))
        except:
            raise Http404
        else:
            try:
                check_version = MyFile.objects.filter(created_at__date = date.today()).values("version").order_by("-version").first()["version"]
                MyFile.objects.create(name = timestamp,file = filename,version = check_version + 1,day_id = id)
            except:
                MyFile.objects.create(name = timestamp,file = filename,day_id = id)
                    
        dtn_load_update(id)
        if id==1:
            return redirect("homeid",1)
        else:
            return redirect("home")
        # return response

        # #creating dictionary for DTN file
       
        # #FTP code

        # return response
        # if id == 0:
        #     return redirect ("home")
        # elif id == 1:
        #     return redirect("homeid",1)
        # else:
        #     return HttpResponseNotFound
    except Exception as e:
        return HttpResponse ("Following error occured during excecution{e}".format(e))
   
        
        
        
        
        