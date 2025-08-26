from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user_app2', null=True, blank=True)

    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('agent', 'Agent'),
        ('admin','Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    terms_and_conditions = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number or 'No Phone Number'
Status_Choices = [
    ('pending', 'Pending'),
    ('approved', 'Approved')
]
class Devices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices', null=True, blank=True)  
    name = models.CharField(max_length=100, null=True, blank=True)
    install_date = models.DateField(auto_now_add=True, null=True, blank=True)
    capacity_kwp = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status_Choices, default='pending', null=True, blank=True)
    tier_field_until = models.CharField(max_length=10, default='0', null=True, blank=True)
    image_field = models.ImageField(upload_to='device_images/', null=True, blank=True)  # ✅ Optional image field

    
    def __str__(self):
        return f"{self.name}"
    
ACCOUNT_TYPES=[
    ('savings account','Savings Account'),
    ('current account','Current Account')
]
BANK_CHOICES = [
    ('brac_bank', 'BRAC Bank'),
    ('dutch_bangla_bank', 'Dutch-Bangla Bank'),
    ('islami_bank', 'Islami Bank'),
    ('city_bank', 'City Bank'),
    ('prime_bank', 'Prime Bank'),
    ('southeast_bank', 'Southeast Bank'),
    ('standard_chartered', 'Standard Chartered'),
]
class BankInformation(models.Model):
    custom_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    nid_number = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Removed the earlier bank_name field (duplicated)
    bank_name = models.CharField(max_length=50, choices=BANK_CHOICES, blank=True, null=True)
    
    account_number = models.CharField(max_length=50, blank=True, null=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, blank=True, null=True)
    branch_code = models.CharField(max_length=150, blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('custom_user', 'account_number')

    def __str__(self):
        return f"{self.custom_user.username} - {self.account_number}"

class BrandInformation(models.Model):
    brand_name=models.CharField(max_length=30,blank=True,null=True)
    brand_image=models.ImageField(upload_to='brand_images/',null=True,blank=True)
    
    def __str__(self):
        return self.brand_name
    

DeviceInformation_Check=[
    ('confirm','Confirm'),
    ('pending','Pending'),
   
]
DeviceInformation_Status=[
    
    ('accepted',"Accepted"),
    ('pending','Pending'),
]
class DeviceInformation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_info', null=True, blank=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='device_info', null=True, blank=True)
    brand_info=models.ForeignKey(BrandInformation, on_delete=models.CASCADE, related_name='device_info', null=True, blank=True)
    device_type=models.CharField(max_length=50,null=True,blank=True)
    capacity=models.DecimalField(max_digits=10,decimal_places=5,null=True,blank=True)
    operations_date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=10,choices=DeviceInformation_Status,default='pending',null=True,blank=True)
    Check=models.CharField(max_length=10,choices=DeviceInformation_Check,default='pending',null=True,blank=True)
    signature=models.ImageField(upload_to='signatures/',null=True,blank=True)

    def __str__(self):
        return f"{self.custom_user}"

class Inverter(models.Model):
    device=models.ForeignKey(DeviceInformation,on_delete=models.CASCADE,related_name='inverters',null=True,blank=True)
    serial_number=models.CharField(max_length=100,null=True,blank=True)
    capacity=models.DecimalField(max_digits=10,decimal_places=5,null=True,blank=True)
    
    def __str__(self):
        return f"{self.serial_number}"
class DeviceLocation(models.Model):
    device=models.ForeignKey(DeviceInformation,on_delete=models.CASCADE,related_name='locations',null=True,blank=True)
    address=models.CharField(max_length=255,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    province=models.CharField(max_length=100,null=True,blank=True)
    postal_code=models.CharField(max_length=20,null=True,blank=True)

    
    def __str__(self):
        return f"{self.address}"


# class UserSign(models.Model):
#     # user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_sign',null=True,blank=True)
#     # custom_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_sign',null=True,blank=True)
#     signature=models.ImageField(upload_to='signatures/',null=True,blank=True)
    