from django.contrib import admin
from .models import Shop, Category, SubCategory, Order, OrderItem

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("title","category",)

class ShopAdmin(admin.ModelAdmin):
    list_display = ("title","subcategory")



admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Shop,ShopAdmin)

admin.site.register(OrderItem)
admin.site.register(Order)