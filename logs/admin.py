from pydoc_data.topics import topics
from django.contrib import admin
from .models import Entry, Topic

# Register your models here.
admin.site.register(Topic)
admin.site.register(Entry)