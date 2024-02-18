from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Very basic structure. To be further built up.
    """

    name = models.CharField(
        _("display name"),
        max_length=150,
        unique=True,
        help_text=_("This will be displayed to user as-is"),
    )
    price = models.PositiveSmallIntegerField(
        _("selling price (Rs.)"),
        help_text=_("Price payable by customer (Rs.)"),
    )
    description = models.TextField(
        _("descriptive write-up"),
        unique=True,
        help_text=_("Few sentences that showcase the appeal of the product"),
    )
    is_refrigerated = models.BooleanField(
        help_text=_("Whether the product needs to be refrigerated"),
        default=False,
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    edited_at = models.DateTimeField(auto_now=True, help_text=_("Timestamp of the most recent edit"))
    ingredients = models.CharField(max_length=500, blank=True, help_text=_("List of ingredients"))

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Rs. {self.price})"

    class Meta:
        # Just to be explicit.
        db_table = "product"
        ordering = []
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField()
    selling_price = models.PositiveSmallIntegerField()
    platform_commission = models.PositiveSmallIntegerField()
    cost_price = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        self.selling_price = self.cost_price + self.platform_commission
        super(Sku, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.size}g"

    def clean(self):
        # Enforce uniqueness for the size field per product
        if Sku.objects.filter(product=self.product, size=self.size).exclude(pk=self.pk).exists():
            raise ValidationError("A SKU with this size already exists for this product.")
