from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=25)
    address=models.TextField()
    profile_pic=ResizedImageField(size=[300,300],upload_to='profile_pics',null=True,blank=True,force_format='webp',quality=100)
DEPT = [
    ('CSE', 'Computer Science & Engineering'),
    ('EEE', 'Electrical & Electronic Engineering'),
    ('BBA', 'Business Administration'),
    ('ENG', 'English Literature'),
]

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    roll_no = models.CharField(max_length=15, unique=True, blank=True, null=True)
    dept = models.CharField(max_length=50, choices=DEPT)
    address = models.TextField()
    profile_pic = ResizedImageField(size=[300, 300], upload_to='profile_pics')
    def __str__(self):
        return self.user.username
