from django.db import models
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

us_state_abbrev = [    ('AL', 'AL'),    ('AK', 'AK'),    ('AZ', 'AZ'),    ('AR', 'AR'),    ('CA', 'CA'),    ('CO', 'CO'),    ('CT', 'CT'),    ('DE', 'DE'),    ('DC', 'DC'),    ('FL', 'FL'),    ('GA', 'GA'),    ('HI', 'HI'),    ('ID', 'ID'),    ('IL', 'IL'),    ('IN', 'IN'),    ('IA', 'IA'),    ('KS', 'KS'),    ('KY', 'KY'),    ('LA', 'LA'),    ('ME', 'ME'),    ('MD', 'MD'),    ('MA', 'MA'),    ('MI', 'MI'),    ('MN', 'MN'),    ('MS', 'MS'),    ('MO', 'MO'),    ('MT', 'MT'),    ('NE', 'NE'),    ('NV', 'NV'),    ('NH', 'NH'),    ('NJ', 'NJ'),    ('NM', 'NM'),    ('NY', 'NY'),    ('NC', 'NC'),    ('ND', 'ND'),    ('OH', 'OH'),    ('OK', 'OK'),    ('OR', 'OR'),    ('PA', 'PA'),    ('RI', 'RI'),    ('SC', 'SC'),    ('SD', 'SD'),    ('TN', 'TN'),    ('TX', 'TX'),    ('UT', 'UT'),    ('VT', 'VT'),    ('VA', 'VA'),    ('WA', 'WA'),    ('WV', 'WV'),    ('WI', 'WI'),    ('WY', 'WY')]

class Terminal(models.Model):
    location = models.CharField(max_length=100,null=False,unique=True,blank=False)
    state = models.CharField(max_length=10,choices= us_state_abbrev)
    location_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.location
    @staticmethod
    def get_location():
        return Terminal.objects.all()
   

class Customer(models.Model):
    customer = models.CharField(max_length=150,null=False,unique= True,blank=False)
    cust_status = models.BooleanField(default=False)
    dtn = models.CharField(max_length = 100,blank = True)
    send_format = models.IntegerField(null = False,blank= False,default=0)
    # DTN = 0
    # Mail = 1
    
    def __str__(self) -> str:
        return self.customer


class Product(models.Model):
    product = models.CharField(max_length=150,null=False,unique= True,blank=False)
    product_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product

class Terminal_customer_mapping(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    location = models.ForeignKey(Terminal,on_delete=models.CASCADE)
    Product =  models.ForeignKey(Product,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{}-{}-{}".format(self.Product,self.location,self.customer)


class Location_price(models.Model):
    location = models.ForeignKey(Terminal,on_delete=models.CASCADE,related_name="locations")
    date = models.DateField(default=date.today,db_index=True)
    price = models.FloatField(default= 0)
    price_dffernce = models.FloatField(default= 0)
    status = models.IntegerField(default=0)

    def __str__(self) -> str:
        return "{}-{}-{}".format(self.location,self.date,self.price)

    @staticmethod
    def get_location_price():
        return Location_price.objects.all().values()       

    def get_location_price_by_date(date):
        # return Location_price.objects.select_related("location_name").filter(date = date).values()
        return Location_price.objects.filter(date = date).values("location__location","date","price","price_dffernce","location")



class Cust_price(models.Model):
    cust_term_prod = models.ForeignKey(Terminal_customer_mapping,on_delete=models.CASCADE)
    date = models.DateField(default=date.today,db_index=True)    
    price_variance = models.FloatField()
    base_price = models.FloatField()
    Final_price = models.FloatField()
    status = models.IntegerField(default=0)
    

    

    def __str__(self) -> str:
        return '{}'.format(self.cust_term_prod_id)


    def get_cust_price_by_date(date):
        return Cust_price.objects.filter(date = date).values()
    
    
class dtn_load(models.Model):
    loadno = models.IntegerField(default=0)   
    date = models.DateField()
    day_id = models.IntegerField(default=0)
    
    

class useraccess(models.Model):
    email = models.CharField(max_length=100,null=False,unique=True)
    email_trigger = models.BooleanField(default=True)
    



class MyFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)
    day_id = models.IntegerField()

    class Meta:
        unique_together = ('name', 'version','created_at')

    def __str__(self) -> str:
        return self.name
#Add user to group while new user signup
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        print(instance.email)
        email = instance.email.lower()
        if useraccess.objects.filter(email = email):
            instance.groups.add(Group.objects.get(name='trader'))
        else:
            print("ksnnwlofjwffjl")    
        