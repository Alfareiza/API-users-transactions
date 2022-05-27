from django.db import models


class Transaction(models.Model):
    reference = models.IntegerField()
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    TYPE_CHOICES = (
        ("outflow", "Outflow"),
        ("inflow", "Inflow"),
    )
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default="outflow"
    )
    category = models.CharField(max_length=15)
    user_email = models.EmailField(max_length=254)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.reference
