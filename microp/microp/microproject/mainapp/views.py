from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Donation, Inventory, Distribution, MoneySpent, Member


# =========================
# INDEX
# =========================
def index(request):
    return render(request, 'mainapp/index.html')


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            auth_login(request, user)
            return redirect('home')
    return render(request, 'mainapp/login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):
    auth_logout(request)
    return redirect('index')


# =========================
# HOME DASHBOARD
# =========================
@login_required
def home(request):
    # MONEY
    money_received = Donation.objects.filter(
        donation_type='Money'
    ).aggregate(total=Sum('amount'))['total'] or 0

    money_spent = MoneySpent.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    money_available = money_received - money_spent

    # INVENTORY
    def available(name):
        return Inventory.objects.filter(
            resource_name=name
        ).aggregate(total=Sum('available_quantity'))['total'] or 0

    food_available = available('Food')
    clothes_available = available('Clothes')
    medicine_available = available('Medicine')
    other_available = available('Other')

    def distributed(name):
        return Distribution.objects.filter(
            resource__resource_name=name
        ).aggregate(total=Sum('quantity'))['total'] or 0

    food_distributed = distributed('Food')
    clothes_distributed = distributed('Clothes')
    medicine_distributed = distributed('Medicine')
    other_distributed = distributed('Other')

    members = Member.objects.filter(is_active=True)

    return render(request, 'mainapp/home.html', {
        'money_received': money_received,
        'money_spent': money_spent,
        'money_available': money_available,

        'food_available': food_available,
        'food_distributed': food_distributed,
        'clothes_available': clothes_available,
        'clothes_distributed': clothes_distributed,
        'medicine_available': medicine_available,
        'medicine_distributed': medicine_distributed,
        'other_available': other_available,
        'other_distributed': other_distributed,

        'members': members,
        'active_members': members.count(),
    })


# =========================
# DONATION (WHAT NGO RECEIVES)
# =========================
def donation(request):
    if request.method == "POST":
        donor_name = request.POST.get('donor_name')
        donation_type = request.POST.get('donation_type')
        amount = int(request.POST.get('amount'))

        # Save donation
        Donation.objects.create(
            donor_name=donor_name,
            donation_type=donation_type,
            amount=amount
        )

        # If resource donation → update inventory
        if donation_type != "Money":
            inventory, _ = Inventory.objects.get_or_create(
                resource_name=donation_type,
                defaults={'available_quantity': 0}
            )
            inventory.available_quantity += amount
            inventory.save()

        return redirect('home')

    return render(request, 'mainapp/donation.html')


# =========================
# NGO CONTRIBUTION (DISTRIBUTION)
# =========================
def resource(request):
    inventories = Inventory.objects.all()

    if request.method == "POST":
        resource_type = request.POST.get('resource_name')
        quantity = int(request.POST.get('quantity'))
        beneficiary_details = request.POST.get('beneficiary_details')

        # MONEY DISTRIBUTION
        if resource_type == "Money":
            money_received = Donation.objects.filter(
                donation_type='Money'
            ).aggregate(total=Sum('amount'))['total'] or 0

            money_spent = MoneySpent.objects.aggregate(
                total=Sum('amount')
            )['total'] or 0

            money_available = money_received - money_spent

            if quantity > money_available:
                return render(request, 'mainapp/resource.html', {
                    'inventories': inventories,
                    'error': 'Not enough money available'
                })

            MoneySpent.objects.create(
                amount=quantity,
                purpose=beneficiary_details
            )

            return redirect('home')

        # RESOURCE DISTRIBUTION
        inventory = Inventory.objects.get(resource_name=resource_type)

        if quantity > inventory.available_quantity:
            return render(request, 'mainapp/resource.html', {
                'inventories': inventories,
                'error': 'Not enough resource available'
            })

        inventory.available_quantity -= quantity
        inventory.save()

        Distribution.objects.create(
            resource=inventory,
            quantity=quantity,
            beneficiary_details=beneficiary_details
        )

        return redirect('home')

    return render(request, 'mainapp/resource.html', {
        'inventories': inventories
    })


# =========================
# REPORT
# =========================
def report(request):
    return render(request, 'mainapp/report.html')


# =========================
# MEMBERS
# =========================
def add_member(request):
    if request.method == "POST":
        Member.objects.create(
            name=request.POST.get('name'),
            role=request.POST.get('role'),
            image=request.POST.get('image'),
            is_active=True
        )
    return redirect('home')


def delete_member(request, member_id):
    Member.objects.filter(id=member_id).delete()
    return redirect('home')


# =========================
# DONATION REPORT
# =========================
def donation_report(request):
    received = Donation.objects.filter(
        donation_type='Money'
    ).aggregate(total=Sum('amount'))['total'] or 0

    spent = MoneySpent.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(request, 'mainapp/donation_report.html', {
        'received': received,
        'spent': spent,
        'balance': received - spent
    })


# =========================
# RESOURCE REPORT
# =========================
def resource_report(request):
    resources = Inventory.objects.all()

    labels = [r.resource_name for r in resources]
    available = [r.available_quantity for r in resources]
    distributed = [
        Distribution.objects.filter(resource=r).aggregate(
            total=Sum('quantity')
        )['total'] or 0 for r in resources
    ]

    return render(request, 'mainapp/resource_report.html', {
        'labels': labels,
        'available': available,
        'distributed': distributed
    })
