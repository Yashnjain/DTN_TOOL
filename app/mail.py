from django.core.mail import send_mail
from .models import Location_price
import pandas as pd
from datetime import date,timedelta
from django.core.mail import EmailMessage
from app.models import MetaData



def mail_send():
    send_mail("TEST","THis is a test","prism.support@biourja.com",["rahul.sakarde@biourja.com","sanskar.gupta@biourja.com"],fail_silently=False)
    
 

def location_price_mail(date = date.today()):
    try :
        l_price  = Location_price.objects.filter(date = date).values("location_id__location","price")
    except Exception as e :
        raise Exception ("Gettimg Error while fetching data {}".format(e))
    else:
        try:    
            df = pd.DataFrame(l_price)
            css = """<style>
                        .class_td_h{
                            background-color:lightgreen;padding:0.75pt;border-style:none solid none none;border-right-width:1pt;border-right-color:black; text-align: center;
                        }
                        .class_p{
                        font-size:11pt;font-family:Calibri,sans-serif;text-align:left;margin:0;
                        
                        }
                        .class_span{
                            color:black;font-size:9pt;font-family:Arial,sans-serif;
                        }
                        .class_td{
                            background-color:white;padding:0 3.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:black;border-bottom-color:black;
                        }
                        .class_td2{
                            background-color:white;padding:0 3.75pt 0 11.25pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:black;border-bottom-color:black;
                        }
                    </style>"""
            tablecontent = ''
            for i in range(len(df)):
                    tablecontent += f"""<tr><td class="class_td">
                    <p align="center" class="class_p"><span class="class_span">{df.iloc[i][0]}</span></p></td>
                    <td class="class_td2">
                    <p align="center" class="class_p"><span class="class_span">{df.iloc[i][1]}</span></p></td></tr>"""   
            table = """<table border="1" cellspacing="0" cellpadding="0" style="border:1pt solid black;">
                        <tbody><tr>
                        <td class="class_td_h">
                        <p  align="center" class="class_p" style="text-align: center;"><b><span class="class_span" >Commodity</span></b></p></td>
                        <td class="class_td_h">
                        <p  align="center" class="class_p" style="text-align: center;"><b><span class="class_span">Price</span></b></p></td></tr>
                        <tr>
                        {}
                        </tr>
                        </tbody>
                        </table>""".format(tablecontent)
            html = css + table         
        except Exception as e:
            raise Exception ("Getting Error while performaing pandas operations {}".format(e))      
        else :
            metadata = MetaData.objects.get(key="INTERNAL_MAIL_LIST") 
            notification_date = date + timedelta(days=1)
            subject = "MarketData Publisher Service Notification For - {}".format(notification_date)
            from_email = "prism.support@biourja.com"
            recipient_list = metadata.value.get('mail')
            fail_silently = False
            html_message = html
            try:
                send_mail(subject=subject,message = "TESTS" ,from_email=from_email,recipient_list=recipient_list,fail_silently=fail_silently,html_message=html_message)
            except Exception as e:
                raise Exception ("Getting error during mail send {}".format(e))
        finally:
            print("mail send successfully")
            
            
            
def customer_mail(subject,body,path,to = ["rahul.sakarde@biourja.com"],bcc =["rahul.sakarde@biourja.com"]):
    try:
        email = EmailMessage(subject= subject,body=body,from_email='prism.support@biourja.com',to=to,bcc=bcc)
        email.attach_file(path)
        email.send()
    except:
        pass
   
   