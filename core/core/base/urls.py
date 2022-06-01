"""URL mappings for the base app (transaction app)"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from core.base.views import TransactionsViewSet, user_email_summary

router = DefaultRouter()
router.register(r"transactions", TransactionsViewSet, basename="transaction")

app_name = "base"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "transactions/<str:user_email>/summary/",
        user_email_summary,
        name="user_email_summary",
    ),
]
