from django.contrib import admin
from .models import Medicine, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)

class MedicineAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Category,CategoryAdmin)
admin.site.register(Medicine,MedicineAdmin)

