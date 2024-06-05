from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Destinations"

    def __str__(self):
        return self.name

class Spots(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE,default=2,verbose_name='Nearby Destination')
    name = models.CharField(max_length=200)    
    description = models.TextField()
    
    

    class Meta:
        verbose_name_plural="Spots"

    def __str__(self):
        return self.name

class Stay(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()    
    cost_per_night = models.DecimalField(max_digits=8, decimal_places=0)    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE,default=1)
    spots = models.ForeignKey(Spots, on_delete=models.CASCADE,default=2)

    class Meta:
        verbose_name_plural = "Stays"

    def __str__(self):
        return self.name

    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user')
    name=models.CharField(max_length=30,default='name')
    age=models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=40,default='address')
    mobile = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='admin')
    name=models.CharField(max_length=30,default='name')
    age=models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=40,default='address')
    mobile = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    title = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    stays = models.ManyToManyField(Stay)    
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_cost= models.DecimalField(max_digits=8, decimal_places=2,default=None)

    class Meta:
        verbose_name_plural = "Trips"
        

    def __str__(self):
        return f"Destination: {self.destination}, Stay: {self.stays}"

class Restaurants(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE,default=1,verbose_name='Nearby Destination')
    spots = models.ForeignKey(Spots, on_delete=models.CASCADE,default=2,verbose_name='Nearby Spots')
    stays = models.ForeignKey(Stay, on_delete=models.CASCADE,default=2,verbose_name='Nearby Stays')

    class Meta:
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.email}'
