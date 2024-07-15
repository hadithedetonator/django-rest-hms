from django.contrib import admin
from .models import Patient, Doctor, Appointment, Payment, RoomAllotment,Service

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Payment)
admin.site.register(RoomAllotment)
admin.site.register(Service)

