from django.contrib import admin
from . models import CustomUser, DocterModel

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(DocterModel)