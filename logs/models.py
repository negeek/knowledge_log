from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    topic = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.topic


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    entry = models.TextField()
    edited = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.entry[:50] + "..."
