from django.db import models
from lawyers.models import Lawyer
from django.conf import settings


class Consultation(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    client_email = models.EmailField()

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.client:
            return f"{self.client.email} - {self.lawyer}"
        return f"{self.client_email} - {self.lawyer}"