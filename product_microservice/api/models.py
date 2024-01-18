from django.db import models


class ProductModel(models.Model):
    product_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.product_name}"
