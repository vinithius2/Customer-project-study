from rest_framework import serializers
from .models import Customer, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Customer
        fields = ('pk', 'first_name', 'last_name', 'email', 'gender', 'company', 'title', 'city')
