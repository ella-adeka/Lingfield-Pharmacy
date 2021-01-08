from django.contrib import admin
from .models import HealthNews, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)

class HealthNewsAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Category,CategoryAdmin)
admin.site.register(HealthNews,HealthNewsAdmin)

