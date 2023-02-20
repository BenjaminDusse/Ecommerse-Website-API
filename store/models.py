from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from uuid import uuid4

from django.conf import settings

from store.validators import validate_file_size

# Promotion  - Product M2M
class Promotion(models.Model):
    """
    Promotion for products

    """

    description = models.CharField(max_length=255)
    discount = models.FloatField()

    class Meta:
        verbose_name = 'Promotions'
        verbose_name_plural = 'Promotion'


class Collection(models.Model):
    """Category for products"""

    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )  # when 2 models are connected in a circle relationship, if it says related name, you should add + to related name

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Collections'
        verbose_name_plural = 'Collection'

class Product(models.Model):
    """Product(item) model"""

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Product'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    caption = models.CharField(max_length=200)
    file = models.ImageField(
        upload_to="store/images",
        validators=[validate_file_size]
    )

    def __str__(self):
        return self.caption

    # Checking file
    # file = models.FileFIeld(
    #     upload_to='store/images',
    #     validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    # )


class Customer(models.Model):
    """Customer in platform"""

    MEMBERSHIP_BRONZE = "Bronze"
    MEMBERSHIP_SILVER = "Silver"
    MEMBERSHIP_GOLD = "Gold"

    MEMBERSHIP_CHOICES = (
        ("B", MEMBERSHIP_BRONZE),
        ("S", MEMBERSHIP_SILVER),
        ("G", MEMBERSHIP_GOLD),
    )

    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=6, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering="user__first_name")
    def first_name(self):
        """Function shows first name of the user in admin panel"""
        return self.user.first_name

    def last_name(self):
        """Function shows last name of the user in admin panel"""
        return self.user.last_name

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        permissions = [("view_history", "Can view history")]
        verbose_name = 'Customers'
        verbose_name_plural = 'Customer'

class Order(models.Model):
    """Order of the customer"""

    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"

    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    )
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, default=PAYMENT_STATUS_PENDING, choices=PAYMENT_STATUS_CHOICES
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [("cancel_order", "Can cancel order")]
        verbose_name = 'Orders'
        verbose_name_plural = 'Order'


class OrderItem(models.Model):
    """Ordered Items of the customers order"""

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orderitems"
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], default=1
    )
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'OrderItems'
        verbose_name_plural = 'OrderItem'
    # def __str__(self):
    #     return f"{self.order} ordered {self.product}"


class Cart(models.Model):
    """Cutomers cart to convert sales, payments, transactions ..."""

    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Carts'
        verbose_name_plural = 'Cart'

class CartItem(models.Model):
    """Items added to cart by customer"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["cart", "product"]]
        verbose_name = 'CartItems'
        verbose_name_plural = 'CartItem'

class Address(models.Model):
    """Customer Address"""

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.customer.user.id}: Street: {self.street}, City: {self.city}"
        )

    class Meta:
        verbose_name = 'Addresses'
        verbose_name_plural = 'Address'

class Review(models.Model):
    """Review model for products page"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Reviews'
        verbose_name_plural = 'Review'
