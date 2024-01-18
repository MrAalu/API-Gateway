from django.db import models


class OrderModel(models.Model):
    order_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.order_name}"
