from django.contrib import admin
from .models import User,Dependent,UserBirthDate, UserProfile, HospitalList, AddSurgery, PrescriptionItem, Prescription

# Register your models here.

admin.site.register(AddSurgery)
admin.site.register(Dependent)
admin.site.register(HospitalList)
admin.site.register(PrescriptionItem)
admin.site.register(Prescription)
admin.site.register(UserBirthDate)
admin.site.register(UserProfile)


