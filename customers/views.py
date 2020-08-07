from rest_framework import viewsets
from .models import Customer
from .serializer import CustomerSerializer


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listing all customers and, another one for getting a single customer by its id
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_fields = ['first_name', 'last_name', 'city', 'company']
    ordering = ['first_name']
    search_fields = ['first_name']
