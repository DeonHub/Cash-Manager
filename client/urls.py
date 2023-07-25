from django import views
from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('<str:mid>/', views.index, name="index"),
    path('<str:mid>/view-assigned-payments/', views.viewAssignedPayments, name="viewAssignedPayments"),
    path('<str:mid>/make-payments/<int:pk>', views.makePayments, name="makePayments"),
    path('<str:mid>/view-detail/<int:pk>', views.viewDetail, name="viewDetail"),
    path('<str:mid>/view-assigned/<int:pk>', views.viewAssigned, name="viewAssigned"),
    path('<str:mid>/view-payments/', views.viewPayments, name="viewPayments"),
    path('<str:clid>/invoice-details-view/<int:pk>', views.invoice_details_view, name="invoice_details_view"),
    path('<str:clid>/donation-details-view/<int:pk>', views.donation_details_view, name="donation_details_view"),


    # path('invoice-details-view/<int:pk>', views.invoice_details_view, name="invoice_details_view"),
    # path('donation-details-view/<int:pk>', views.donation_details_view, name="donation_details_view"),
    # path('profile/', views.viewProfile, name="viewProfile"),
    # path('pay-online/', views.payOnline, name="payOnline"),
    path('<str:mid>/logout/', views.logout, name="logout"),

    # path('view-donation/<int:id>', views.viewDonation, name="viewDonation"),
    path('pay-donation/<int:id>', views.payDonation, name="payDonation"),
    
    path('ajax/load_bill/', views.load_bill, name='ajax_load_bill'),
    path('ajax/delete_payment/', views.delete_payment, name='ajax_delete_payment'),
    # path('ajax/delete_assigned/', views.delete_assigned, name='ajax_delete_assigned'),

    path('<str:mid>/client-profile/', views.viewProfile, name="viewProfile"),
    # path('home/', views.home, name="home"),
]