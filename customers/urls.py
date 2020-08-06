# Django Imports
from django.conf.urls import include
from django.urls import path

# Third Party Imports
from rest_framework.routers import DefaultRouter

# Local Imports
from customers.views import CustomerViewSet

router = DefaultRouter()
router.register(r'', CustomerViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
