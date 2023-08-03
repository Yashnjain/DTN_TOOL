from django.shortcuts import render,redirect
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from app.models import   Terminal_customer_mapping,Location_price,Cust_price,dtn_load

from  datetime import date 
from datetime import timedelta
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test

import csv
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User,Group,GroupManager
from django.core.mail import send_mail
from app.mail import mail_send,location_price_mail
from app.utils import authorisation,setdate,dtn_load_update
import logging
from django.views.decorators.csrf import csrf_exempt
import time
logger = logging.getLogger(__name__)




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
        
        # To Track the active page
        color = True
        if id == 1:
            color = False   
        
        # getting the latest dtn upload No,else setting else false for insert case.
        try:
            maxstatus = dtn_load.objects.filter(date= today).values("loadno").order_by("-loadno").first()["loadno"]
        except:
            maxstatus = False
        
        if request.method == 'GET':
            logging.info("##########################<Inside GET METHOD>############################")
            #Get t-1 date data based on id 
            locations_price_yesterday = Location_price.get_location_price_by_date(date = yesterday)
            #Get t date data 
            locations_price_today = Location_price.get_location_price_by_date(date = today)
            
            #Check for T date data 
            submit_active = False
            if locations_price_today: 
                print("Todays data is already there")
                submit_active = True
                
                
                
            #Adding Tth date price i.e New price
            def addtodayprice(location_price_yesterday):
               
                print(location_price_yesterday["location"])
                for location_price_today in locations_price_today:
                    if location_price_today["location"] == location_price_yesterday["location"]:          
                        return (location_price_today.get("price",0),location_price_today.get("price_dffernce",0))  
                    # return (0,0)

            location_and_customer = []
            for location_price_yesterday in locations_price_yesterday:
                # looping through all the location
                location_result = {}
                location_result["location_name"] = location_price_yesterday["location__location"]
                location_result["yesterday_price"] = round(location_price_yesterday["price"],4)
                location_result["price_diff"] =  round(location_price_yesterday["price_dffernce"],4)
                location_result["location_id"] = str(location_price_yesterday["location"])
                if locations_price_today: 
                    
                    # print(addtodayprice(location_price_yesterday))
                    # check for current date or Tth date data if exits otherwise leave it take only previous day data 
                    try :
                        location_result["new_price"],location_result["price_diff"] = addtodayprice(location_price_yesterday)

                    except : 
                        location_result["new_price"],location_result["price_diff"] = (0,0)  
                if location_result["location_id"]:
                    # getting mapping of customer for given location
                    tcpmappings  = Terminal_customer_mapping.objects.filter(location = location_result["location_id"]).values("id","customer_id__customer","customer_id","status")
                    customer_detail = [] 
                    for tcp in tcpmappings:
                        # looping through all the mapping         
                        customer_result ={}
                        customer_result["customer_name"] = tcp["customer_id__customer"]
                        customer_result["status"] = tcp["status"]   
                        ctpm = tcp["id"]
                        customer_result["ctpm"] = str(ctpm)         
                        try:
                            
                            if locations_price_today:    
                                if Cust_price.objects.filter(date = today,cust_term_prod_id = ctpm):
                                    customer_prices_yesterday = Cust_price.objects.filter(date = today,cust_term_prod_id = ctpm).values("price_variance")[0]
                                else:
                                    customer_prices_yesterday = Cust_price.objects.filter(date = yesterday,cust_term_prod_id = ctpm).values("price_variance")[0]     
                            else:
                                print("check")
                                if Cust_price.objects.filter(date = yesterday,cust_term_prod_id = ctpm).values("price_variance")[0]:
                                    customer_prices_yesterday = Cust_price.objects.filter(date = yesterday,cust_term_prod_id = ctpm).values("price_variance")[0]   
                                
                        except:
                            pass  
                        try:
                            customer_result["price_variance"] = customer_prices_yesterday["price_variance"]
                        except:
                            customer_result["price_variance"] = 0 
                        customer_detail.append(customer_result)
                        
                    location_result["customer"] = customer_detail    
                location_and_customer.append(location_result)
            context = {
               "l_y_p" : location_and_customer,
               "active" : color,
               "submit_active" : submit_active,
               "dtnloadsubmit" : maxstatus
            }
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Total time taken: {total_time} seconds")
            
            return render (request,"Home1_updated.html",context)
            
        elif request.method == 'POST':
            logging.info("##########################<Inside GET METHOD>############################")
            # yesterday = date.today() - timedelta(days=1)
            # today = date.today() 
            
            # Getting post data 
            data = request.POST
            print(data)
            
            # Dictionary for post data filteration
            location = {}
            price_variance = {}
            cptm = {}
            
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
                    else:
                        pass
                except ValueError:
                    
                    # print("888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888")
                    raise ValidationError("Enter Valid Data as float or int kindly check if there blank box reload the page and try again",code="500")       
            
            try:
                maxstatus = dtn_load.objects.filter(date= today).values("loadno").order_by("-loadno").first()["loadno"]
            except:
                maxstatus = False    
            for key,value in location.items():
                location_yesterday_price = Location_price.objects.filter(date = yesterday,location_id = key).values_list("price")[0][0]
                locations_price_today = Location_price.get_location_price_by_date(today)
                # if locations_price_today:
                l_price = Location_price.objects.filter(location_id = key,date = today).first()
                if l_price:
                    location_price = round(float(location_yesterday_price) + float(value),4)
                    if l_price.price_dffernce != round(float(value),4):
                        l_price.price_dffernce = round(float(value),4)
                        l_price.price = round(float(location_yesterday_price) + float(value),4)
                        if maxstatus:
                            l_price.status = int(maxstatus) + 1
                        l_price.save()
                else:
                    location_price = round(float(location_yesterday_price) + float(value),4)
                    l_price = Location_price(location_id = key,date = today,price =round((float(location_yesterday_price) + float(value)),4),price_dffernce = round(float(value),4))
                    l_price.save()
                tcpmappings  = Terminal_customer_mapping.objects.filter(location = key)
                # print("###########################################################################################")
                for tcp in tcpmappings:
                    if str(tcp.id) in list(cptm.keys()):
                        print("inside tcp")
                        tcp.status = True
                        tcp.save()
                    else:
                        tcp.status = False
                        tcp.save()
                    
                    if str(tcp.id) in list(price_variance.keys()):
                        print("insied customer")
                        discount  = float(price_variance[str(tcp.id)])
                        print(discount)
                        # cust_price_today = Cust_price.objects.filter(date= date.today())
                        # if cust_price_today:
                        #     print("today")

                        customer_price = Cust_price.objects.filter(date= today,cust_term_prod_id = tcp.id).first()
                        if customer_price:
                            if customer_price.price_variance != round(discount,4):
                                customer_price.price_variance = round(discount,4)
                                if maxstatus:
                                    customer_price.status = int(maxstatus) + 1
                            if customer_price.Final_price != round((float(location_price) + discount),4):
                                customer_price.Final_price = round((float(location_price) + discount),4)
                                if maxstatus:
                                    customer_price.status = int(maxstatus) + 1
                            
                            customer_price.save()
                        else:
                            # print("check")
                            
                            c_p = Cust_price(date= today,price_variance = round(discount,4),Final_price = round((float(location_price) + discount),4),cust_term_prod_id = tcp.id)
                            if maxstatus:
                                c_p.status = maxstatus + 1
                            c_p.save()
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
        print(e)
        return HttpResponse ("Getting follwing {} error kindly check".format(e))



@login_required(login_url="/accounts/microsoft/login")
@authorisation
def mainpage(request):
    if request.method == 'GET':
        try:
            # print(today_price)
            today_date = date.today()
            yesterday = str(today_date - timedelta(days = 1))
            # l_y_p : location yesterday price
            # l_t_p : location today price
            #  c_y_p : costomer yesterday price
            #  c_y_t :  costomer today price
            l_y_p = Location_price.get_location_price_by_date(yesterday)
            l_t_p = Location_price.get_location_price_by_date(today_date)
              
               


         
            
            if l_t_p:
                today_p = []
                today_dif =[]
                for i in l_t_p:
                    today_p.append(i["price"])
                    today_dif.append(i["price_dffernce"])
                count = 0    
                for j in l_y_p:
                    try:
                       j["new_price"] = today_p[count]
                       j["price_dffernce"] = today_dif[count]
                    except:
                        print("check exception")  
                    
                    count +=1
                return render(request, "index.html" ,{"l_y_p" : l_y_p })




            return render(request, "index.html",{"l_y_p" : l_y_p})
        except Exception as e:
            print(e)
            return HttpResponse ("error")    
    elif request.method == 'POST':
        try:
            yesterday = str(date.today() - timedelta(days = 1))
            location_price = Location_price.objects.filter(date = yesterday).values_list("location_id","price")
            return HttpResponse("checking ")
            for location in location_price:
                price_diff = request.POST.get(str(location[0]),None)
                print(location[1],price_diff)
                l_price = Location_price(location_id = location[0],date = date.today(),price = (float(location[1]) + float(price_diff)),price_dffernce = price_diff)
                l_price.save()
                print(price_diff)

            print("________________________________")
            return redirect("home")
        except Exception as e:
            print(e)
            return HttpResponse ("unsuccess")
            


def strformat(s):
    return "'{}'".format(s)


def genrate_dtn_file(dtnlist : dict,dtncodedict : dict):  
    effective_date = date.today()
    effective_date = effective_date.strftime("%m/%d/%y")
    print(effective_date)
    f = open("dtn_sample.csv",'w', newline='')
    c = csv.writer(f)
    data = []
    idpass = ["ABC1","PASSWORD"]
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
           
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==")
            print(lp["location"],key)
        c.writerow(note)
        c.writerow(end)
        #i = i + 1
        


@login_required(login_url="/accounts/microsoft/login")
@authorisation
def fetch_dtn_file_data(request,id,for_date):
    try:
        # dtnlist = []
        # cps = customers price 
        supplier = {} 
        dtn = {}
        if id == 1:
             dtn_load_status = dtn_load.objects.filter(date = for_date).order_by("-loadno").values("loadno").first()["loadno"]
            
        
        try:
            dtn_load_status = dtn_load.objects.filter(date = for_date).order_by("-loadno").values("loadno").first()["loadno"]
          #  dtn_load_status =  dtn_load.objects.filter(date= for_date).values("loadno").order_by("-loadno").first()["load_no"]
        except:
            dtn_load_status = False
        if dtn_load_status:
            cps = Cust_price.objects.filter(date = for_date,status = (dtn_load_status + 1) ).values()
        else:     
        cps = Cust_price.objects.filter(date = for_date).values()
        if cps:
            for cp in cps:
                
                # print((cp["cust_term_prod_id"]))
                if cp:
                    clms = Terminal_customer_mapping.objects.filter(id = cp["cust_term_prod_id"],status = True).values("location_id","customer__customer","customer__dtn")
                    if clms:
                        location_list = []
                        for clm in clms:
                            if clm["customer__customer"] in dtn.keys():
                                pass
                            else:
                                dtn[clm["customer__customer"]] = clm["customer__dtn"]
                            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@S')
                            if clm["customer__customer"] in supplier.keys():
                                pass
                            else:
                                supplier[clm["customer__customer"]] = []
                            
                            if clm:
                                lps = Location_price.objects.filter(location_id = clm["location_id"],date = for_date).values("price","location_id__location","price_dffernce","location_id__state")
                                if lps:
                                    for lp in lps:
                                        if lp:
                                            print('check')
                                            loc = dict()
                                            loc["state"] = lp["location_id__state"]
                                            loc["location"] = lp["location_id__location"]
                                            loc["price"] = cp["Final_price"]
                                            loc["change"] = lp["price_dffernce"] + cp["price_variance"]
                                            loc["effective_date"] = date.today()
                                            loc["effective_time"] = "18:00"
                                           
                                            print("check2")
                                            supplier[clm["customer__customer"]].append(loc)
                                      
        return HttpResponse ("pass")  
    except Exception as e:
        print("fail")
        return HttpResponse (e) 
    finally:
        print(supplier)
        genrate_dtn_file(supplier,dtn)
   


   
@login_required(login_url="/accounts/microsoft/login")
@authorisation
def load_data_to_dtn(request,id = 0):
    for_date = None
    if id == 0:
        for_date = date.today()  
    elif id == 1 :
        print("yesterday")
        for_date = date.today() - timedelta(days=1)
    else:
        return HttpResponseNotFound    
        
    check = None   
    try:
       
        fetch_dtn_file_data(request,id,for_date)       
        # location_price_mail(for_date)
        dtn_load_update(for_date)

        #creating dictionary for DTN file
       
        #FTP code

        
        if id == 0:
            return redirect ("home")
        elif id == 1:
            return redirect("homeid",1)
        else:
            return HttpResponseNotFound
    except Exception as e:
        return HttpResponse ("Following error occured during excecution{e}".format(e))
   
        
        
        
        
        