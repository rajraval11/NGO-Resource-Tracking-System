from django.contrib import admin
from .models import Donation, Inventory, Distribution, Member

admin.site.register(Donation)
admin.site.register(Inventory)
admin.site.register(Distribution)
admin.site.register(Member)
