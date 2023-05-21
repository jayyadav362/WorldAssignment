from django.contrib import admin
from account.models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(OTP)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Countrylanguage)