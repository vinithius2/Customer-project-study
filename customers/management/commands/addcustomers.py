# Python Imports
import csv

# Local Imports
from customers.constants import GENDERS_DICT

# Django Imports
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
# Project Imports
from customers.models import Customer
from customers.models import City


class Command(BaseCommand):
    """
    Get a csv file and input in database
    """
    help = 'Add customers with cvs file'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Please wait...'))
        for path in options['path']:
            try:
                customer_list = self.get_list_customer(path)
                Customer.objects.bulk_create(customer_list)
            except FileNotFoundError as error:
                self.stdout.write(self.style.ERROR('Do you need a valid file!'))
                raise CommandError(f"FileNotFoundError: {error}")
            except IntegrityError as error:
                self.stdout.write(self.style.ERROR(
                    'Your csv file exist a row with ID existing in database!'))
                raise CommandError(f"IntegrityError: {error}")
            self.stdout.write(self.style.SUCCESS('Successfully!'))

    def get_list_customer(self, path):
        with open(path, 'r', newline='') as csvfile:
            customer_list = list()
            total = 0
            count = 0
            for row in csv.DictReader(csvfile, skipinitialspace=True):
                city, created = City.objects.get_or_create(name=row["city"])
                row["city"] = city
                row["gender"] = GENDERS_DICT[row["gender"]]
                customer_list.append(Customer(**row))
                count = count + 1
                if count >= 25:
                    total = total + count
                    count = 0
                    self.stdout.write(self.style.WARNING(f'Get {total} rows...'))
            self.stdout.write(self.style.WARNING(f'Saving {len(customer_list)} models...'))
            return customer_list
