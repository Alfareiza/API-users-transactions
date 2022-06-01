"""
Serializers for transaction APIs
"""
from rest_framework import serializers

from core.base.models import Transaction
from core.base.validators import validate_amount, validate_reference


class TransactionsSerializer(serializers.ModelSerializer):
    """Serializer for Transactions."""

    class Meta:
        model = Transaction
        fields = [
            "id",
            "reference",
            "date",
            "type",
            "amount",
            "category",
            "user_email",
        ]
        # exclude = ['id', 'created_at']
        validators = [validate_amount, validate_reference]


class TransactionsGroupedbyType(serializers.Serializer):
    """ "Serializer for transaction group by"""

    total_inflow = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_outflow = serializers.DecimalField(max_digits=12, decimal_places=2)
    user_email = serializers.EmailField(max_length=254)
