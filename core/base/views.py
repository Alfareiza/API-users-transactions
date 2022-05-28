from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from core.base.models import Transaction
from core.base.serializers import TransactionsSerializer


def home(request):
    return HttpResponse('<h1>Hello World</h1>')


class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
