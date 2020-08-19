# Python Imports
import csv

# Local Imports
from customers.constants import GENDERS_DICT

# Django Imports
from django.core.management.base import BaseCommand, CommandError

# Project Imports
from customers.models import Customer, City


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
            except TypeError as error:
                raise CommandError(f"TypeError: {error}")
            except Exception as error:
                raise CommandError(f"Exception: {error}")
            self.stdout.write(self.style.SUCCESS('Successfully!'))

    def get_list_customer(self, path):
        with open(path, 'r', newline='') as csvfile:
            customer_list = list()
            total = 0
            count = 0
            for row in csv.DictReader(csvfile, skipinitialspace=True):
                city, created = City.objects.get_or_create(name=row["city"])
                row["id"] = int(row["id"])
                row["city"] = city
                row["gender"] = GENDERS_DICT[row["gender"]]
                customer_list.append(Customer(dict(row)))
                count = count + 1
                if count >= 25:
                    total = total + count
                    count = 0
                    self.stdout.write(self.style.WARNING(f'Get {total} rows...'))
            self.stdout.write(self.style.WARNING(f'Saving {len(customer_list)} models...'))
            return customer_list
