from django.contrib import admin

# Register your models here.
from user.models import user, BookTable

admin.site.register(user)
admin.site.register(BookTable)