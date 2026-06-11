from django.db import models


# =========================
# DONATION MODEL
# =========================
class Donation(models.Model):
    DONATION_CHOICES = [
        ('Money', 'Money'),
        ('Food', 'Food'),
        ('Clothes', 'Clothes'),
        ('Medicine', 'Medicine'),
        ('Other', 'Other'),
    ]

    donor_name = models.CharField(max_length=100)
    donation_type = models.CharField(max_length=20, choices=DONATION_CHOICES)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.donor_name} - {self.donation_type}"


# =========================
# INVENTORY MODEL
# =========================
class Inventory(models.Model):
    resource_name = models.CharField(max_length=50, unique=True)
    available_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.resource_name} - {self.available_quantity}"


# =========================
# DISTRIBUTION MODEL
# =========================
class Distribution(models.Model):
    resource = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    beneficiary_details = models.CharField(max_length=200)
    distributed_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource.resource_name} - {self.quantity}"


# =========================
# MONEY SPENT MODEL
# =========================
class MoneySpent(models.Model):
    purpose = models.CharField(max_length=200)
    amount = models.IntegerField()
    spent_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.purpose} - ₹{self.amount}"


# =========================
# MEMBER MODEL
# =========================
class Member(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
