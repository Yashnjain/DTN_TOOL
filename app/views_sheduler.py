import csv
import os
import threading
from datetime import date, datetime, timedelta

from django.conf import settings
from django.http import Http404, HttpResponse

from .excel import create_excel_file
from .fpt import transfer_files
from .mail import customer_mail, location_price_mail
from .models import MyFile
from .utils import dtn_load_update, strformat,validate_user
from .views import fetch_dtn_file_data

@validate_user
def sheduler(requests):
    try:
        id = 0
        today = date.today()
        
        dtnlist,dtncodedict,dtnlist_email,mail_list = fetch_dtn_file_data(id,today)
        ###################################### FILE CREATION ################################################## 
    
        effective_date = date.today() + timedelta(days=1)
        effective_date = effective_date.strftime("%m/%d/%y")
        update  = False
        if dtnlist:
            response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="Dtnfile.csv"'},
                    )
            c = csv.writer(response,delimiter=',',
                        lineterminator='\r\n',
                        quotechar = "'",quoting=csv.QUOTE_MINIMAL)
                # c = csv.writer(response,doublequote=True,quoting=csv.QUOTE_NONNUMERIC, quotechar='"',delimiter= ",")
            idpass = ["BUR1","URJA"]
            messagetype  =  ["PRF"]
            commandline = ["C02","0001","  /  /  ","00:00","0000","1","0001","S","$"]
            dtncode = ['0008']
            begin = ["BEGIN-BINARY-DATA"]
            header = [strformat("HEADER"),strformat(str("BioUrja Trading LLC"))]
                # detail_item = [strformat("PRICE"),"Terminal","statecode",strformat("Magellan"),"Ethanol","product_price","change amount",effective_date,"00:01"]
            detail_item = [strformat("PRICE"),"Terminal","statecode",strformat("Magellan"),strformat("Ethanol"),"product_price","",effective_date,"00:01"]
            note  = [strformat("NOTE"),strformat("FOR QUESTIONS PLEASE CONTACT 012-345-6789  DTN@example.com")]
            end = ["END-BINARY-DATA"]
            eof = ["<!--END OF FILE-->"]
            c.writerow(idpass)
            c.writerow(messagetype)
            seq = 1
            for key,value in dtnlist.items():
                commandline[1] = str(seq).zfill(4)
                c.writerow(commandline)
                dtncode[0] = dtncodedict[key]
                if "," in dtncode[0]:
                    dtncode_list = dtncode[0].split(",")
                    c.writerow(dtncode_list)
                else:        
                    c.writerow(dtncode)
                c.writerow(begin)
                    # for getting coustomer 
                    # header[1] = strformat(key)  
                note[1] = strformat(key)
                c.writerow(header)
                for lp  in value:
                    detail_item[1] = strformat(lp["location"])
                    detail_item[2] = strformat(lp["state"])
                    detail_item[5] = (format((lp["price"]),".4f"))
                    c.writerow(detail_item)
                c.writerow(note)
                c.writerow(end) 
                seq = seq + 1       
            c.writerow(eof)
            timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            filename = "{}.csv".format(timestamp)
            file_path = os.path.join(settings.MEDIA_ROOT,"files",filename)
            try:
                with open(file_path, 'w',newline='') as f:
                    f.write(response.content.decode('utf-8'))
                        # f.write(response.content.decode('utf-8-sig'))        
            except:
                raise Http404
            else:
                try: 
                    check_version = MyFile.objects.filter(created_at__date = date.today(),day_id = id).values("version").order_by("-version").first()["version"]
                    MyFile.objects.create(name = timestamp,file = filename,version = check_version + 1,day_id = id)
                except:
                    MyFile.objects.create(name = timestamp,file = filename,day_id = id)
            update = True  
            ############################## FILE TRANSFER #############################
            transfer_files(file_path)  
        ##################################### FOR NON DTN NON SUBSCRIBER USER ###################################################
        if dtnlist_email:  
            def mass_mail():
                try:
                    for key,value in dtnlist_email.items():
                        path = os.path.join(settings.MEDIA_ROOT,"files_mail",f"BioUrja_Magellan_Price_{key}_{str(date.today())}.xlsx")
                        create_excel_file(location_prices=value,effective_date=effective_date,path = path)
                        subject = f"BioUrja Trading - Magellan Price for {str(date.today())}"
                        body = f"BioUrja_Magellan_Price_{key}_{str(date.today())}"
                        if mail_list[key][0] and mail_list[key][1]:
                            customer_mail(subject,body,path,to=mail_list[key][0].split(','),bcc = mail_list[key][1].split(',') )   
                    if id == 1:
                        location_price_mail(date.today() - timedelta(days=1))
                    else:
                        location_price_mail(date.today())
                except Exception as e:
                    raise Exception (e)
                    
            thread = threading.Thread(target=mass_mail)    
            thread.start()
            update = True
        if update:
            dtn_load_update(id) 
            return HttpResponse('SUCCESS')    
        else:
            return HttpResponse("NO DATA FOR UPLOAD")
    except Exception as e:
        return HttpResponse(e)
