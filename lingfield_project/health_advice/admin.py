from django.contrib import admin
from .models import HealthAdvice, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)

class HealthAdviceAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Category,CategoryAdmin)
admin.site.register(HealthAdvice,HealthAdviceAdmin)

