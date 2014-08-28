from django.contrib.gis import admin
from models import account

admin.site.register(account, admin.GeoModelAdmin)

