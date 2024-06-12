from django.db import models
from django.contrib.auth.models import User

class Counsellor(models.Model):
      user=models.ForeignKey(User,on_delete=models.CASCADE)
      center=models.CharField(max_length=255)
      joining_date=models.DateField(null=True)
      photo=models.ImageField(upload_to='images',blank=True,null=True)
      status=models.BooleanField(default=True)

class Lead(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    date = models.DateField()
    source_of_lead = models.CharField(max_length=100)
    counsellor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    mode = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    joining_centre = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    education_background = models.CharField(max_length=50)
    main = models.TextField(blank=True, null=True)
    cs_background = models.CharField(max_length=3)
    employed = models.BooleanField()
    joining_month = models.CharField(max_length=20)
    additional_notes = models.TextField(blank=True, null=True)
    initial_response = models.TextField(blank=True, null=True)
    first_follow_up = models.TextField(blank=True, null=True)
    first_follow_up_date = models.DateField(blank=True, null=True)
    second_follow_up = models.TextField(blank=True, null=True)
    second_follow_up_date = models.DateField(blank=True, null=True)
    third_follow_up = models.TextField(blank=True, null=True)
    third_follow_up_date = models.DateField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.phone_number}'
         
class login_details(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     time=models.DateTimeField(auto_now=True)
     browser=models.CharField(max_length=255,null=True)
     browser_version=models.CharField(max_length=255,null=True)
     os=models.CharField(max_length=255,null=True)
     os_version=models.CharField(max_length=255,null=True)
     device=models.CharField(max_length=255,null=True)
     is_mobile=models.BooleanField(default=False)
     is_tablet=models.BooleanField(default=False)
     is_pc=models.BooleanField(default=False)
     is_bot=models.BooleanField(default=False)
