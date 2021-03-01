from django.contrib import admin
from .models import *

# Register your models here.
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ("user","get_medicine_items","selected_surgery")

    def get_medicine_items(self, obj):
        return "\n,".join([str(i)for i in obj.medicine_items.all()])

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("user","get_prescription_items")

    def get_prescription_items(self, obj):
        # return "\n".join([str(i)for i in obj.items.all()])
        return "\n".join([i.medicine_item for i in obj.items.all()])



# admin.site.register(Category,CategoryAdmin)

admin.site.register(AddSurgery)
admin.site.register(Dependent)
admin.site.register(HospitalList)
admin.site.register(MedicineItems)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(PrescriptionItem, PrescriptionItemAdmin)
admin.site.register(SelectSurgery)
admin.site.register(UserBirthDate)
admin.site.register(UserProfile)


