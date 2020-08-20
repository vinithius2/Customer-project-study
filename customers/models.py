# Python Imports
from urllib import parse
from urllib import request
import json

# Local Imports
from customers.constants import GENDERS

# Django Imports
from django.conf import settings
from django.db import models
from django.core.exceptions import PermissionDenied
from django.core.management.base import CommandError


class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Looking for latitude and longitude before save model
        in Google API with address available
        """
        parm = parse.urlencode({"address": self.name})
        try:
            req = request.Request(
                f"{settings.URL_GOOGLE_MAPS}?{parm}&key={settings.API_KEY}")
            response = request.urlopen(req)
            if response.status == 200:
                result = json.load(response)
                if 'REQUEST_DENIED' == result['status']:
                    raise PermissionDenied(result['error_message'])
                self.latitude = result["results"][0]["geometry"]["location"]["lat"]
                self.longitude = result["results"][0]["geometry"]["location"]["lng"]
        except TimeoutError as error:
            raise CommandError(f"TimeoutError: {error}")
        except PermissionDenied as error:
            raise CommandError(f"PermissionDenied: {error}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDERS)
    company = models.CharField(max_length=50)
    title = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
