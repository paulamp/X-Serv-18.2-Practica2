from django.db import models

# Create your models here.

class Url(models.Model):
    url = models.CharField(max_length=200, unique=True)
    short_url = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return '%s: %s' % (self.url, self.short_url)
