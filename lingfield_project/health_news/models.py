from django.db import models
from django.shortcuts import reverse
from djrichtextfield.models import RichTextField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20,unique=False)
    slug = models.SlugField()
   
    class Meta():
        
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' #a,b,c,d...

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("health_news:health-news-list-by-category", args=[self.slug])

  
  
class HealthNews(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,unique=False)
    list_description = models.CharField(max_length=1000)
    detail_description =  models.TextField(max_length=1000000)
    slug = models.SlugField()

    class Meta():
        ordering = ['title']
        verbose_name = 'Health News'
        verbose_name_plural = 'Health News' #a,b,c,d...
       
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("health_news:health-news-detail", args=[self.id,])