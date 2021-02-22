from django.db import models
from django.shortcuts import reverse
from djrichtextfield.models import RichTextField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20,unique=False)
    slug = models.SlugField(unique=False)
   
    class Meta():
        ordering = ['title']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' #a,b,c,d...

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("health_advice:health-advice-list", kwargs={
            'slug' : self.slug
        })

  
    
class HealthAdvice(models.Model):
    category = models.ForeignKey(Category, verbose_name="Category",on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,unique=False)
    list_description = models.CharField(max_length=1000)
    detail_description =  models.TextField(max_length=100000000)
    slug = models.SlugField()

    class Meta():
        ordering = ['title']
        verbose_name = 'Health Advice'
        verbose_name_plural = 'Health Advices' #a,b,c,d...

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("health_advice:health-advice-detail", kwargs={
            'slug' : self.slug
        })