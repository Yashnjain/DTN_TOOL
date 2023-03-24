from django.core.mail import send_mail
from .models import Location_price
import pandas as pd
from datetime import date 
from django.contrib.sessions.models import Session


from django.contrib.sites.models import Site
def mail_send():
    send_mail("TEST","THis is a test","itdevsupport@biourja.com",["rahul.sakarde@gmail.com.com"],fail_silently=False)
    
 

def location_price_mail(date = date.today()):
    try :
        l_price  = Location_price.objects.filter(date = date).values("location_id__location","price")
    except Exception as e :
        raise Exception ("Gettimg Error while fetching data {}".format(e))
    else:
        try:    
            df = pd.DataFrame(l_price)
            print(df)
            # df.columns = ["Commodity","price"]
            # df = df.reset_index(drop=True)
            html =  df.to_html()  
            
            
        except Exception as e:
            raise Exception ("Getting Error while performaing pandas operations {}".format(e))      
        else :
            subject = "MarketData Publisher Service Notification For - {}".format(date)
            from_email = "itdevsupport@biourja.com"
            recipient_list = ["rahul.sakarde@biourja.com"]
            fail_silently = False
            html_message = html
            try:
                send_mail(subject=subject,message = "TESTS" ,from_email=from_email,recipient_list=recipient_list,fail_silently=fail_silently,html_message=html_message)
            except Exception as e:
                raise Exception ("Getting error during mail send {}".format(e))
        finally:
            print("mail send successfully")
            
            
            
            
            
            
        