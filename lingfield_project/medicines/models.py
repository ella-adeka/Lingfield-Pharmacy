from django.db import models
from django.shortcuts import reverse
from djrichtextfield.models import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20,unique=False)
    slug = models.SlugField()

    class Meta():
        ordering = ['title']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' #a,b,c,d...

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("medicines:medicine-category-detail", kwargs={
            'slug' : self.slug
        })


class Medicine(models.Model):
    category = models.ForeignKey(Category, verbose_name="Category",on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,unique=False)
    list_description = models.CharField(max_length=1000)
    detail_description =  models.TextField(max_length=1000000)
    slug = models.SlugField()

    class Meta():
        ordering = ['title']
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines' #a,b,c,d...

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("medicines:medicine-detail", kwargs={
            'slug' : self.slug
        })

    def get_medicine_url(self):
        return reverse("accounts:item", kwargs={
            'slug' : self.slug
        })