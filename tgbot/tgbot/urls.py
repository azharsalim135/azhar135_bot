"""tgbot URL Configuration

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
from django.urls import path
from azhar135_bot import urls as azhar135_bot_urls
from django.urls import include, re_path
from django.db import OperationalError, connections
import psycopg2
from psycopg2 import sql
import itertools


urlpatterns = [
    path('admin/', admin.site.urls),
    path('azhar135_bot/', include(azhar135_bot_urls)),
]

conn = connections['default']
try:
    c = conn.cursor() #this will take some time if error
    c.execute("CREATE TABLE IF NOT EXISTS button_count (btn_name varchar(45) NOT NULL,btn_count integer NOT NULL);")
    c.execute("create TABLE IF NOT EXISTS user_data ( user_id char(50) primary key not null,no_of_calls int);")    #Create tables if not exists


    query_check_table="SELECT btn_name from button_count"
    c.execute(query_check_table)
    check_table_list=c.fetchall()

    check_table_list= list(itertools.chain(*check_table_list)) # convert list of tuple into list -> to check if the requires columns are there in the table
    print(check_table_list)
    orginal_list = ['fat', 'stupid', 'dumb'] 
    print("\n",orginal_list)

    if not all(value in check_table_list for value in orginal_list): #check if all the coumns are there in the table, if not re-initialize
        
        print("Something missing\n")
        query="TRUNCATE button_count; DELETE FROM button_count;" #reset table to empty
        c.execute(query)
        query="INSERT INTO button_count (btn_name,btn_count) VALUES('fat',0),('dumb',0),('stupid',0)" #initialize table
        c.execute(query)
        print("TABLE RE-INITALIZED\n")

    c.close()
    conn.close()
except OperationalError:
    reachable = False
else:
    reachable = True