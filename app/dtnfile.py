import csv

from datetime import date

dtnlist = {'ApexOil': [{'state': 'MN', 'location': 'Alexandria', 'price': 6.0, 'change': 6.0, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'IL', 'location': 'Amboy', 'price': 0.1, 'change': 0.1, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'CO', 'location': 'Aurora', 'price': 23.5, 'change': 23.5, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'MO', 'location': 'Carthage', 'price': 35.6, 'change': 35.6, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'IL', 'location': 'Chicago', 'price': 12.0, 'change': 12.0, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}], 'Atlas': [{'state': 'MN', 'location': 'Alexandria', 'price': 58.0, 'change': 58.0, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'IL', 'location': 'Amboy', 'price': 0.1, 'change': 0.1, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'CO', 'location': 'Aurora', 'price': 36.5, 'change': 36.5, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'MO', 'location': 'Carthage', 'price': 24.8, 'change': 24.8, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}], 'AOT': [{'state': 'CO', 'location': 'Aurora', 'price': 24.5, 'change': 24.5, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'MO', 'location': 'Carthage', 'price': 24.6, 'change': 24.6, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'IL', 'location': 'Chicago', 'price': 11.5, 'change': 11.5, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}], 'Ayers': [{'state': 'CO', 'location': 'Aurora', 'price': 23.5, 'change': 23.5, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}, {'state': 'MO', 'location': 'Carthage', 'price': 23.6, 'change': 23.6, 'effective_date': (2023, 2, 15), 'effective_time': '18:00'}]}


f = open("samplee.csv",'w', newline='')
c = csv.writer(f)



print()

data = []
idpass = ["ABC1","PASSWORD"]
messagetype  =  ["PRF"]
commandline = ["CO2","0001"," / / ","00:00","0000","1","0001","S","$"]
dtncode = ['0008']
begin = ["BEGIN-BINARY-DATA"]
header = ["HEADER","Customername"]
detail_item = ["price","Terminal","statecode","MAG","partner_name","productname","product_price","change amount",date.today(),"18:00"]
note  = ["NOTE","FOR QUESTIONS PLEASE CONTACT 012-345-6789, DTN@example.com"]
end = ["END-BINARY-DATA"]





c.writerow(idpass)
c.writerow(messagetype)
for key,value in dtnlist.items():
    i = 1
    commandline[1] = "000{}".format(i)
    
    c.writerow(commandline)
    c.writerow(dtncode)
    c.writerow(begin)
    header[1] = key
    c.writerow(header)
    for lp  in value:
        print(lp)
        detail_item[1] = lp["location"]
        detail_item[2] = lp["state"]
        detail_item[6] = lp["price"]
        detail_item[7] = lp["change"]
        c.writerow(detail_item)
        print(detail_item)
        print(len(data))
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==")
    c.writerow(note)
    c.writerow(end)
    i+=1
    print(data)
print(data)    
# f = open("samplee.csv",'w', newline='')
# c = csv.writer(f)
# c.writerows(data)






