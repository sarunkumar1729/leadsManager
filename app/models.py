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
    date = models.DateField(auto_now=True)
    source_of_lead = models.CharField(max_length=100)
    counsellor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    mode = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    joining_centre = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    education_background = models.CharField(max_length=50)
    main = models.TextField(blank=True, null=True)
    cs_background = models.BooleanField(default=True)
    employed = models.BooleanField()
    joining_month = models.CharField(max_length=20)
    additional_notes = models.TextField(blank=True, null=True,default=None)
    initial_response = models.TextField(blank=True, null=True,default=None)
    first_follow_up = models.TextField(blank=True, null=True,default=None)
    first_follow_up_date = models.DateField(blank=True, null=True,default=None)
    second_follow_up = models.TextField(blank=True, null=True,default=None)
    second_follow_up_date = models.DateField(blank=True, null=True,default=None)
    third_follow_up = models.TextField(blank=True, null=True,default=None)
    third_follow_up_date = models.DateField(blank=True, null=True,default=None)
    last_modified = models.DateTimeField(auto_now=True)
    editing=models.BooleanField(default=False)

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

class notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    phone = models.CharField(max_length=255,null=True)
    date = models.DateField(auto_now_add=True,null=True)
    time = models.TimeField(auto_now_add=True,null=True)