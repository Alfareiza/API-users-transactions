from rest_framework import serializers

from core.base.models import Transaction
from core.base.validators import validate_amount, validate_reference


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        # fields = ['reference', 'date', 'type', 'amount', 'category', 'user_email']
        exclude = ['id', 'created_at']

    validators = [
        validate_amount,
        validate_reference,
    ]
