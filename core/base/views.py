"""
Views for the Transaction APIs
"""

from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.base.models import Transaction
from core.base.resources import (
    calc_summary_user,
    group_types_by_user_email,
)
from core.base.serializers import (
    TransactionsSerializer,
    TransactionsGroupedbyType,
)


def home(request):
    """
    Once the user try to acess to the homepage, will be redirect
    to the API DRF Home Page.
    """
    return HttpResponseRedirect(reverse('base:transaction-list'))


class TransactionsViewSet(viewsets.ModelViewSet):
    """View for manage transaction APIs."""

    serializer_class = TransactionsSerializer
    queryset = Transaction.objects.all()
    http_method_names = ["get", "post", "delete", "put", "head"]

    def get_queryset(self):
        if self.request.query_params.get("group_by", False) == "type":
            queryset = Transaction.objects.raw(
                "Select id, user_email, "
                "SUM(CASE WHEN type == 'outflow' THEN amount ELSE 0 END) "
                "as total_outflow,  "
                "SUM(CASE WHEN type == 'inflow' THEN amount ELSE 0 END)"
                "as total_inflow "
                "from BASE_TRANSACTION group by user_email"
            )
            result = group_types_by_user_email(queryset)
            self.serializer_class = TransactionsGroupedbyType
            return result
        else:
            return self.queryset.order_by("created_at")

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


@api_view(["GET"])
def user_email_summary(request, user_email):
    """Get a summary of a specific user"""
    # http://127.0.0.1:8000/api/v1/transactions/janedoe@email.com/summary/
    transaction = Transaction.objects.filter(user_email__iexact=user_email)
    result = {"user_email": f"User '{user_email}' doesn't exists."}
    if transaction:
        result = calc_summary_user(transaction)
    return Response(result)
