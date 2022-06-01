from decimal import Decimal
from django.test import TestCase

from core.base.models import Transaction


class ModelTests(TestCase):
    """Test Models"""

    def test_create_transaction_model(self):
        transaction = Transaction.objects.create(
            reference="000001",
            date="2022-05-02",
            type="outflow",
            amount=Decimal("-150.00"),
            category="transfer",
            user_email="janedoe@email.com",
        )
        self.assertEqual(str(transaction), transaction.reference)
