from django.urls import path

from core.base.views import call_transactions

urlpatterns = [
    path('v1/transactions', call_transactions, name='call_transactions')
]
