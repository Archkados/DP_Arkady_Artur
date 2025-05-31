from django.contrib import admin
from .models import *

admin.site.register(Person)
admin.site.register(CarNumber)
admin.site.register(Visa)
admin.site.register(TruckInsurance)
admin.site.register(TrailerInsurance)
admin.site.register(TruckInspection)
admin.site.register(TrailerInspection)
admin.site.register(Company)
admin.site.register(SubCompany)
admin.site.register(FreightCompany)
admin.site.register(Route)
admin.site.register(ShippingApplication)
admin.site.register(TrackingRequest)
admin.site.register(Stage)
admin.site.register(StageTemplate)
admin.site.register(CargoInfo)
admin.site.register(TrailerNumber)

