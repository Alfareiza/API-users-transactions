from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.base.models import Transaction
from core.base.resources import (
    calc_summary_user,
    group_types_by_user_email,
)
from core.base.serializers import (
    TransactionsSerializer,
    TransactionsGroupedbyType,
)

TRANSACTION_URL = reverse("base:transaction-list")


def detail_url(transaction_id):
    """Create and return a transaction detail URL."""
    return reverse("base:transaction-detail", args=[transaction_id])


def create_transaction(**kwargs):
    """Create and return a sample transaction"""
    defaults = dict(
        reference="000001",
        date="2022-05-02",
        type="outflow",
        amount=Decimal("-150.00"),
        category="transfer",
        user_email="janedoe@email.com",
    )
    defaults.update(kwargs)
    return Transaction.objects.create(**defaults)


class TransactionAPITests(TestCase):
    """Test API Requests"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_transactions(self):
        """Test retrieving a list o transactions."""
        create_transaction(
            reference="000001",
            date="2022-05-07",
            type="outflow",
            amount=Decimal("-1294.65"),
            category="rent",
            user_email="janedoe@email.com",
        )
        create_transaction(
            reference="000002",
            date="2022-05-03",
            type="inflow",
            amount=Decimal("1500.00"),
            category="salary",
            user_email="janedoe@email.com",
        )
        res = self.client.get(TRANSACTION_URL)
        transactions = Transaction.objects.all().order_by("created_at")
        serializer = TransactionsSerializer(transactions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_transaction_detail(self):
        """Test get transaction detail."""
        transaction = create_transaction()

        url = detail_url(transaction.id)  # /api/v1/transactions/1/
        res = self.client.get(url)
        serializer = TransactionsSerializer(transaction)

        self.assertEqual(res.data, serializer.data)

    def test_create_transaction(self):
        """Test creating a transaction"""
        payload = dict(
            reference="000002",
            date="2022-05-03",
            type="inflow",
            amount=Decimal("1500.00"),
            category="salary",
            user_email="janedoe@email.com",
        )

        res = self.client.post(
            TRANSACTION_URL, payload
        )  # /api/v1/transactions/
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_full_update(self):
        """Test full update of transaction."""
        transaction = create_transaction()
        payload = dict(
            reference="000002",
            date="2022-05-08",
            type="inflow",
            amount=Decimal("1000.00"),
            category="bonus",
            user_email="janedoe@email.com",
        )

        url = detail_url(transaction.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()

        # Assert of every attr
        self.assertEqual(transaction.reference, payload["reference"])
        self.assertEqual(
            transaction.date,
            datetime.strptime(payload["date"], "%Y-%m-%d").date(),
        )
        self.assertEqual(transaction.type, payload["type"])
        self.assertEqual(transaction.amount, payload["amount"])
        self.assertEqual(transaction.category, payload["category"])
        self.assertEqual(transaction.user_email, payload["user_email"])

    def test_delete_transaction(self):
        """Test deleting a transaction successful"""
        transaction = create_transaction()
        url = detail_url(transaction.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Transaction.objects.filter(id=transaction.id).exists()
        )

    def test_user_email_summary(self):
        """Test summary of specific user"""
        specific_user = "janedoe@email.com"
        create_transaction(
            reference="000001",
            date="2022-05-07",
            type="outflow",
            amount=Decimal("-1000.00"),
            category="rent",
            user_email=specific_user,
        )
        create_transaction(
            reference="000002",
            date="2022-05-07",
            type="outflow",
            amount=Decimal("-20.10"),
            category="groceries",
            user_email=specific_user,
        )
        create_transaction(
            reference="000003",
            date="2022-05-07",
            type="inflow",
            amount=Decimal("500.00"),
            category="savings",
            user_email=specific_user,
        )
        create_transaction(
            reference="000004",
            type="inflow",
            amount=Decimal("2000.00"),
            category="salary",
            user_email=specific_user,
        )

        res = self.client.get(
            reverse("base:user_email_summary", args=[specific_user])
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        transaction = Transaction.objects.filter(
            user_email__iexact=specific_user
        )
        self.assertEqual(res.data, calc_summary_user(transaction))

        # Testing when user_email doesnt exists on db
        unknown_user = "qwerty@email.com"
        res = self.client.get(
            reverse("base:user_email_summary", args=[unknown_user])
        )
        transaction = Transaction.objects.filter(
            user_email__iexact=unknown_user
        )
        self.assertEqual(
            res.data, {"user_email": f"User '{unknown_user}' doesn't exists."}
        )

        # Testing operations in the summary
        create_transaction(
            reference="000005",
            type="outflow",
            amount=Decimal("-30.90"),
            category="groceries",
            user_email=specific_user,
        )
        transaction = Transaction.objects.filter(
            user_email__iexact=specific_user
        )
        self.assertEqual(
            Decimal("-51.00"),
            calc_summary_user(transaction)["outflow"]["groceries"],
        )

    def test_group_by_type(self):
        """Test query param group by type"""
        user_one = "janedoe@email.com"
        user_two = "foobar@email.com"
        create_transaction(
            reference="000001",
            type="outflow",
            amount=Decimal("-1000.00"),
            category="rent",
            user_email=user_one,
        )
        create_transaction(
            reference="000002",
            type="outflow",
            amount=Decimal("-20.10"),
            category="groceries",
            user_email=user_one,
        )
        create_transaction(
            reference="000003",
            type="inflow",
            amount=Decimal("500.00"),
            category="savings",
            user_email=user_one,
        )
        create_transaction(
            reference="000004",
            type="inflow",
            amount=Decimal("2000.00"),
            category="salary",
            user_email=user_one,
        )
        create_transaction(
            reference="000005",
            type="outflow",
            amount=Decimal("-776.41"),
            category="rent",
            user_email=user_two,
        )
        create_transaction(
            reference="000006",
            type="outflow",
            amount=Decimal("-75.10"),
            category="groceries",
            user_email=user_two,
        )
        create_transaction(
            reference="000007",
            type="inflow",
            amount=Decimal("334.00"),
            category="savings",
            user_email=user_two,
        )
        create_transaction(
            reference="000008",
            type="inflow",
            amount=Decimal("1789.90"),
            category="salary",
            user_email=user_two,
        )

        res = self.client.get(TRANSACTION_URL, {"group_by": "type"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        queryset = Transaction.objects.raw(
            "Select id, user_email, "
            "SUM(CASE WHEN type == 'outflow' THEN amount ELSE 0 END) \
            as total_outflow,  "
            "SUM(CASE WHEN type == 'inflow' THEN amount ELSE 0 END) \
            as total_inflow "
            "from BASE_TRANSACTION group by user_email"
        )
        result = group_types_by_user_email(queryset)
        serializer = TransactionsGroupedbyType(result, many=True)

        self.assertEqual(res.data, serializer.data)
