from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(NewUser)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(JobList)
admin.site.register(WorkDetails)

