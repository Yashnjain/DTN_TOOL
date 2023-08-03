import csv
from django.http import HttpResponse
from django.db import connection
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from app.utils import validate_user



@login_required(login_url="/accounts/microsoft/login")
def download_csv(request, current_date = False):
    # Execute the SQL query
    try:    
        if not current_date:
            current_date = str(date.today())
            
        with connection.cursor() as cursor:
            query = f"""SELECT cp.date as Date, tm.location_code as Terminal, 
                        ac.customer_code as CustCode, ac.company as CustName,
                        CASE
                            WHEN atcm.rack THEN alp.price
                            ELSE cp."Final_price"
                        END AS Price
                    FROM public.app_cust_price AS cp
                    INNER JOIN app_terminal_customer_mapping AS atcm ON cp.cust_term_prod_id = atcm.id
                    INNER JOIN app_terminal AS tm ON atcm.location_id = tm.id
                    INNER JOIN app_location_price AS alp ON tm.id = alp.location_id
                    INNER JOIN app_customer AS ac ON atcm.customer_id = ac.id
                    WHERE cp.date = '{current_date}' AND alp.date = '{current_date}' and ac.sap = true ;"""
            cursor.execute(query)
            rows = cursor.fetchall()
        if len(rows) == 0:
            return HttpResponse(f"Data not updated for the date {current_date}")
        # Create a response object
        response = HttpResponse(content_type='text/csv')
        filename = f'price_{current_date}.csv'
        response['Content-Disposition'] = f'attachment; filename= {filename}'

        # Write the query result to the response as CSV
        writer = csv.writer(response)
        writer.writerow([column[0] for column in cursor.description])  # Write column headers
        writer.writerows(rows)  # Write the query result rows

        return response
    except Exception as e :
        return HttpResponse(e)