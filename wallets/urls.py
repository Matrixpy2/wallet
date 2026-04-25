from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import MywalletsApi

router =DefaultRouter()
router.register('wallet' , MywalletsApi , 'wallet')

urlpatterns = [
    path('' , include(router.urls)),
]