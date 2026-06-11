from django.urls import path
from . import views

urlpatterns = [
    # Index
    path('index/', views.index, name='index'),

    # Home
    path('home/', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Donations & Resources
    path('donation/', views.donation, name='donation'),
    path('resource/', views.resource, name='resource'),

    # Reports
    path('report/', views.report, name='report'),
    path('report/donations/', views.donation_report, name='donation_report'),
    path('report/resources/', views.resource_report, name='resource_report'),

    # Members
    path('add-member/', views.add_member, name='add_member'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
]
