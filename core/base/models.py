from django.db import models
from rest_framework.exceptions import ValidationError


class Transaction(models.Model):
    reference = models.CharField(max_length=6, unique=True)
    date = models.DateField()
    TYPE_CHOICES = (
        ("outflow", "Outflow"),
        ("inflow", "Inflow"),
    )
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default="outflow"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2,
                                 validators=[])
    category = models.CharField(max_length=15)
    user_email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True, )

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return str(self.reference)

    def clean(self):
        if self.type == 'outflow' and self.amount > 0:
            raise ValidationError('Outflow entries doesn\'t must be positive.')
        # Set the pub_date for published items if it hasn't been set already.
        if self.type == 'inflow' and self.amount < 0:
            raise ValidationError('Inflow entries doesn\'t must be negative.')
        if not self.reference.isnumeric():
            raise ValidationError('Reference must be contain only numbers.')
