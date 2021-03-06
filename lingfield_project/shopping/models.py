from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from djrichtextfield.models import RichTextField
from django.utils import timezone

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    date_paid = models.DateTimeField(auto_now_add=True)
    
class Category(models.Model):
    title = models.CharField(max_length=50,unique=False)
    slug = models.SlugField(max_length=1000, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['title']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' #a,b,c,d...

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shopping:product-list-by-category", args=[self.slug])

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=1000, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['title']
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories' #a,b,c,d...

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shopping:product-list-by-subcategory",args=[self.slug])


class Shop(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name='shops',)
    title = models.CharField(max_length=1000,unique=False)
    image = models.ImageField(upload_to='shop_products')
    price = models.FloatField()
    old_price = models.FloatField(blank=True, null=True)
    first_description = models.TextField(max_length=1000000)
    second_description =  models.TextField(max_length=1000000)
    directions =  models.TextField(max_length=1000000)
    warnings =  models.TextField(max_length=1000000)
    ingredients =  models.TextField(max_length=1000000)
    slug = models.SlugField()
    total_excl_vat = models.FloatField()
    vat = models.FloatField()
    shipping_cost = models.FloatField()

    class Meta():
        ordering = ['title']
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops' #a,b,c,d...

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shopping:product_detail", kwargs={
            'slug' : self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("shopping:add_to_cart", kwargs={
            'slug' : self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("shopping:remove_from_cart", kwargs={
            'slug' : self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item =  models.ForeignKey(Shop, on_delete=models.CASCADE)
    item_quantity = models.IntegerField(default=1, null=True, blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return "{} of {}".format(self.item_quantity,self.item.title)
        
    def get_total_items_price(self):
        return self.item_quantity * self.item.price 

    def get_total_items_price_with_excl_vat(self):
        return self.item_quantity  * self.item.total_excl_vat

    def get_total_items_price_with_vat(self):
        return self.item_quantity  * self.item.vat

    def get_total_items_price_with_shipping_cost(self):
        return self.item_quantity  * self.item.shipping_cost

    def get_total_discount_items_price(self):
        return self.item_quantity * self.item.old_price

    def get_amount_saved(self):
        return self.get_total_items_price() - self.get_total_discount_items_price()

    def get_price_total(self):
        return self.get_total_items_price() 

    def get_grand_price_total(self):
        return self.get_total_items_price() + self.get_total_items_price_with_shipping_cost() + self.get_total_items_price_with_vat() + self.get_total_items_price_with_excl_vat()
        + self.get_total_discount_items_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_price_total() 
        return total
    
    def get_grand_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_grand_price_total() 
        return total

    def get_total_discount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return total

    def get_total_excl_vat(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_items_price_with_excl_vat() 
        return total

    def get_total_vat(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_items_price_with_vat()
        return total
    
    def get_total_shopping_cost(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_items_price_with_shipping_cost()
        return total

    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for items in orderitems])
        return total

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.item_quantity for items in orderitems])
        return total

