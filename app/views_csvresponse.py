# import csv
# from django.http import HttpResponse
# from app.models import Product
# def my_csv_view(request):
#     # Query your data
#     my_data = Product.objects.all()

#     # Create a CSV response
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="my_data.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['product'])

#     for row in my_data:
#         writer.writerow([row.product])

#     # Convert the response to a CSV file
#     with open('my_data.csv', 'w') as csvfile:
#         csvfile.write(response.content.decode('utf-8'))

#     return response



from django.http import HttpResponse
from app.models import MyFile


def getfiledetail(request):
    files_meta_info = MyFile.objects.all().values()
    return HttpResponse (files_meta_info) 
    
