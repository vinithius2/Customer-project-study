# Python Imports
from urllib import request, parse
import json
# Third Party Imports

# Local Imports
from .constants import GENDERS

# Django Imports
from django.conf import settings
from django.db import models
from django.core.validators import EmailValidator

# Project Imports


def email_validation(value):
    validator = EmailValidator()
    validator(value)
    return value


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, validators=[email_validation])
    gender = models.CharField(max_length=1, choices=GENDERS)
    company = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    title = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Looking for latitude and longitude before save model
        """
        parm = parse.urlencode({"address": self.city})
        req = request.Request(
            f"{settings.URL_GOOGLE_MAPS}?{parm}&key={settings.API_KEY}")
        response = request.urlopen(req)
        if response.status == 200:
            result = json.load(response)
            self.latitude = result["results"][0]["geometry"]["location"]["lat"]
            self.longitude = result["results"][0]["geometry"]["location"]["lng"]
        super(Customer, self).save(*args, **kwargs)
