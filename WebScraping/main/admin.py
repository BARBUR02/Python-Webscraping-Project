from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Offert,CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('id','email','username','first_name','last_name','phone_number','is_admin')
    search_fields = ('id','email','username','first_name','last_name','phone_number')
    # readonly_fields = ('id')
    exclude = ('date_joined','last_login')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Offert)