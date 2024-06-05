from django.contrib import admin
from .models import Trip, Destination, Stay,UserProfile,AdminProfile,Restaurants,Spots,Contact

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'cost_per_night']
    search_fields = ['name']

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name','address','mobile']
    search_fields=['name']

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name','address','mobile']
    search_fields=['name']

@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display= ['id','name','description','destination_id','spots_id','stays_id']
    search_fields=['name','destination_id','spots_id','stays_id']

@admin.register(Spots)
class SpotsAdmin(admin.ModelAdmin):
    list_display=['id','name','description','destination_id']
    search_fields=['name','destination_id']
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=['id','name','email','message']