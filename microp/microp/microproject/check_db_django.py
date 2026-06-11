import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'microproject.settings')
django.setup()

from mainapp.models import Donation, Inventory, Distribution, MoneySpent, Member

print("=== DATABASE CHECK ===")

print("\nDonations:")
for d in Donation.objects.all():
    print(f"  {d}")

print("\nInventory:")
for i in Inventory.objects.all():
    print(f"  {i}")

print("\nDistributions:")
for dist in Distribution.objects.all():
    print(f"  {dist}")

print("\nMoney Spent:")
for ms in MoneySpent.objects.all():
    print(f"  {ms}")

print("\nMembers:")
for m in Member.objects.all():
    print(f"  {m}")

print("\n=== END CHECK ===")
