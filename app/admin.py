from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from .models import Terminal, Customer, Product, Terminal_customer_mapping,Location_price,Cust_price,useraccess,MyFile,dtn_load
from  datetime import date
from datetime import timedelta


day = 1

class CustomerAdmin(admin.ModelAdmin):
    list_filter = ["customer"]
    def save_model(self, request, obj, form, change):
        # First, save the customer object
        super().save_model(request, obj, form, change)

        # Then, create a mapping with all products and terminals
        terminals = Terminal.objects.all()
        products = Product.objects.all()
        for terminal in terminals:
            for product in products:
                mapping = Terminal_customer_mapping(customer = obj, location=terminal, Product=product)
                mapping.save()
                cust_price = Cust_price(cust_term_prod = mapping,date = (date.today() - timedelta(days=day)),price_variance = 0 ,Final_price=0)
                cust_price.save()





class TerminalAdmin(admin.ModelAdmin):
    list_filter = ["location"]
    def save_model(self, request, obj, form, change):
        # First, save the customer object
        super().save_model(request, obj, form, change)
        mapping = Location_price(location = obj,date = (date.today() - timedelta(days=day)),price = 0 ,price_dffernce=0)
        mapping.save()
        customer = Customer.objects.all()
        Products = Product.objects.all()
        for cust in customer:
            for product in Products:
                mapping = Terminal_customer_mapping(customer = cust, location=obj, Product=product)
                mapping.save()
                cust_price = Cust_price(cust_term_prod = mapping,date = (date.today() - timedelta(days=day)),price_variance = 0 ,Final_price=0)
                cust_price.save()
        


class Location_priceAdmin(admin.ModelAdmin):
    list_display = ["location","date","price","price_dffernce"]
    list_filter = ["date"]

class Terminal_customer_mappingAdmin(admin.ModelAdmin):
    list_display = ["customer","location","Product","status"]
    list_filter = ["customer","location","Product","status"]


class Cust_priceAdmin(admin.ModelAdmin):
    list_display = ["cust_term_prod","date","price_variance","Final_price","status"]
    list_filter = ["date","status","cust_term_prod"]

class dtn_loadAdmin(admin.ModelAdmin):
    list_display = ["loadno","date","day_id"]
    list_filter = ["date"]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Terminal_customer_mapping,Terminal_customer_mappingAdmin)
admin.site.register(Terminal,TerminalAdmin)
admin.site.register(Location_price,Location_priceAdmin)
admin.site.register(Cust_price,Cust_priceAdmin)
admin.site.register(Product)
admin.site.register(useraccess)
admin.site.register(MyFile)
admin.site.register(dtn_load,dtn_loadAdmin)


