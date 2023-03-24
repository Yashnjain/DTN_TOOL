"""price_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .viewspeedupdated import home,fetch_dtn_file_data,load_data_to_dtn,download_file,filter_files
from .views_csvresponse import getfiledetail
from .views_delete import reset_today_price

urlpatterns = [ 
    path("",home,name = "home"),
    path("<int:id>",home,name = "homeid"),
    path("submit",load_data_to_dtn ,name = "dtnload"),
    path("submit/<int:id>",load_data_to_dtn ,name = "dtnload"),
    path("file",fetch_dtn_file_data),
    path("reset",reset_today_price),
    path("csv",getfiledetail),
    path("get/<int:id>",download_file),
    path("files",filter_files)
]
  

