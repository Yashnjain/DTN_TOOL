import csv
from django.http import HttpResponse
from django.db import connection
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from app.utils import validate_user



@validate_user
def test(request):
    return HttpResponse('asfjhbsdjksdbn')