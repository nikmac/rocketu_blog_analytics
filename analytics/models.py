from django.db import models
from localflavor.us.models import USStateField


class Page(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return u"{}".format(self.url)


class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    class Meta:
        unique_together = ['city', 'country', 'region']

    def __unicode__(self):
        return u"{}, {} {}".format(self.city, self.country, self.region)


class View(models.Model):
    page = models.ForeignKey(Page)
    location = models.ForeignKey(Location, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    ip_address = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return u"{} by {} @ {}".format(self.ip_address, self.location, self.timestamp)


class Advertisement(models.Model):
    image = models.ImageField(upload_to='blog/static/img')
    url = models.URLField()
    name = models.CharField(max_length=100)
    state = USStateField()

