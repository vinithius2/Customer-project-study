# Python Imports
from urllib import request, parse
import json
import csv
import copy

# Third Party Imports

# Local Imports

# Django Imports
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Project Imports
from customers.models import Customer


class Command(BaseCommand):
    """
    https://docs.djangoproject.com/pt-br/3.0/howto/custom-management-commands/
    """
    help = 'Add customers with cvs file'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Please wait...'))
        for path in options['path']:
            try:
                with open(path, 'r', newline='') as csvfile:
                    has_header = csv.Sniffer().has_header(csvfile.read(1024))
                    csvfile.seek(0)
                    reader = csv.reader(csvfile)
                    if has_header:
                        next(reader)
                    customer_list = list()
                    total = 0
                    for row in reader:
                        customer = Customer(
                            first_name=row[1],
                            last_name=row[2],
                            email=row[3],
                            gender=row[4],
                            company=row[5],
                            city=row[6],
                            title=row[7]
                        )
                        parm = parse.urlencode({"address": customer.city})
                        req = request.Request(
                            f"{settings.URL_GOOGLE_MAPS}?{parm}&key={settings.API_KEY}")
                        response = request.urlopen(req)
                        if response.status == 200:
                            result = json.load(response)
                            customer.latitude = result["results"][0]["geometry"]["location"]["lat"]
                            customer.longitude = result["results"][0]["geometry"]["location"]["lng"]
                        else:
                            self.stdout.write(
                                self.style.ERROR('Error looking for lat and lng of "%s"'
                                                 % customer.city))
                        customer_list.append(customer)
                        if reader.line_num >= total:
                            self.stdout.write(self.style.WARNING(f'Get {reader.line_num} rows...'))
                            total += 25
                    self.stdout.write(self.style.WARNING(f'Saving models...'))
                    Customer.objects.bulk_create(customer_list)
            except FileNotFoundError as e:
                self.stdout.write(self.style.ERROR('Do you need a valid file!'))
                raise CommandError(e)
            except TimeoutError as e:
                self.stdout.write(self.style.ERROR("API Google maps don't work!"))
                raise CommandError(e)
            except Exception as e:
                raise CommandError(e)
            self.stdout.write(self.style.SUCCESS('Successfully!'))
