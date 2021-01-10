from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from medicines.models import Medicine

# Create your models here.
class UserBirthDate(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, related_name="userbirthdate")
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(UserBirthDate, self).save(*args, **kwargs)
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="userprofile")
    telephone_no = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    nhs_no = models.CharField(max_length=10000)
    country = CountryField()
    uk_postcode_lookup = models.CharField(max_length=100)
    house_number = models.CharField(max_length=1000)
    street = models.CharField(max_length=2000)
    town = models.CharField(max_length=1000)
    county = models.CharField(max_length=1000)
    postcode = models.CharField(max_length=1000)
    one_click_purchasing = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)


class Dependent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="dependent", null=True)
    relation = models.CharField(max_length=1000)
    first_name = models.CharField(max_length=1000)
    middle_names = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    birth_date = models.DateField(null=True, blank=True)
    landline_telephone_no = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    nhs_no = models.CharField(max_length=10000)
    notes = models.TextField(max_length=100000)
    country = CountryField()
    street = models.CharField(max_length=2000)
    town = models.CharField(max_length=1000)
    county = models.CharField(max_length=1000)
    postcode = models.CharField(max_length=1000)

    # def __str__(self):
    #     return self.user.username

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        super(Dependent, self).save(*args, **kwargs)
        
class HospitalList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=1000)
    hospital = models.CharField(max_length=1000)
    hospital_street = models.CharField(max_length=1000)
    district = models.CharField(max_length=1000, blank=True)
    city = models.CharField(max_length=1000)
    postal_code = models.CharField(max_length=500)
    slug = models.SlugField()

    def __str__(self):
        return self.clinic_name

    def get_surgery(self):
        return "{}".format(self.clinic_name)
        
    def get_absolute_url(self):
        return reverse("accounts:dashboard-with-surgery", kwargs={
            'slug' : self.slug
        })

    def get_surgery_url(self):
        return reverse("accounts:hospital", kwargs={
            'slug' : self.slug
        })

    def save(self, *args, **kwargs):
        super(HospitalList, self).save(*args, **kwargs)

class AddSurgery(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="addsurgery")
    surgery_name = models.CharField(max_length=1000)
    country = CountryField()
    uk_postcode_lookup = models.CharField(max_length=100)
    house_number = models.CharField(max_length=1000)
    address = models.CharField(max_length=2000)
    
    class Meta():
        verbose_name = 'Add Surgery'
        verbose_name_plural = 'Add Surgeries'

    def __str__(self):
        return "{}'s surgeries".format(self.user.username)

    def __str__(self):
        return self.surgery_name
    
    # def get_surgery(self):
    #     return "{}".format(self.surgery_name)

    def save(self, *args, **kwargs):
        super(AddSurgery, self).save(*args, **kwargs) 

class SelectSurgery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    surgery = models.ForeignKey(HospitalList, on_delete=models.CASCADE)
    added = models.BooleanField(default=False)

    def __str__(self):
        return self.surgery.clinic_name

    
class PrescriptionItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalList, on_delete=models.CASCADE, related_name="prescription_items")
    prescription_item = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="prescription_items")
    prescription_quantity =  models.IntegerField(default=1, null=True, blank=True) 
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return "{} of {}".format(self.prescription_quantity,self.prescription_item)
    
    # def get_new_prescription(self):
    #     return

    def get_hospital(self):
        return self.hospital

    # def get_remove_hospital(self):
    #     return delete self.hospital

class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(PrescriptionItem)
    date_ordered = models.DateTimeField()    
    ordered = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


