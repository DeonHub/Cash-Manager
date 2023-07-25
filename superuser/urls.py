# from django import views
from django.urls import path
from . import views
from . import context_processors

app_name = 'superuser'

urlpatterns = [
    # path('', views.login, name="login"),
    path('', views.index, name="index"),

    path('create-fee-type/', views.createFeeType, name="createFeeType"),
    path('view-fee-type/', views.viewFeeType, name="viewFeeType"),
    path('edit-fee-type/<int:id>/', views.editFeeType, name='editFeeType'),
    path('delete-fee-type/<int:id>', views.deleteFeeType, name='deleteFeeType'),


    path('create-fee-items/', views.createFeeItems, name="createFeeItems"),
    path('view-fee-items/', views.viewFeeItems, name="viewFeeItems"),
    path('edit-fee-item/<int:id>/', views.editFeeItem, name='editFeeItem'),
    path('delete-fee-item/<int:id>/', views.deleteFeeItem, name='deleteFeeItem'),


    path('create-fee-description/', views.createFeeDescription, name="createFeeDescription"),
    path('view-fee-description/', views.viewFeeDescription, name="viewFeeDescription"),
    path('edit-fee-description/<int:id>', views.editFeeDescription, name='editFeeDescription'),
    path('delete-fee-description/<int:id>', views.deleteFeeDescription, name='deleteFeeDescription'),


    path('create-currency/', views.createCurrency, name="createCurrency"),
    path('view-currency/', views.viewCurrency, name="viewCurrency"),
    path('edit-currency/<int:id>', views.editCurrency, name='editCurrency'),
    path('delete-currency/<int:id>', views.deleteCurrency, name='deleteCurrency'),


    path('set-invoice-details/', views.setInvoiceDetails, name="setInvoiceDetails"),
    path('view-invoice-details/', views.viewInvoiceDetails, name="viewInvoiceDetails"),
    path('edit-invoice-details/<int:id>', views.editInvoiceDetails, name='editInvoiceDetails'),
    path('delete-invoice-details/<int:id>', views.deleteInvoiceDetails, name='deleteInvoiceDetails'),


    path('create-invoice/', views.createInvoice, name="createInvoice"),
    path('view-invoice/', views.viewInvoice, name="viewInvoice"),
    path('edit-invoice/<int:id>', views.editInvoice, name='editInvoice'),
    path('view-codes/', views.viewAccessCodes, name='viewAccessCodes'),
    
    # path('delete-invoice/<int:id>', views.deleteInvoice, name='deleteInvoice'),


    # path('create-donation/', views.createDonation, name="createDonation"),
    # path('view-donations/', views.viewDonations, name="viewDonations"),
    # path('view-donation/<int:id>', views.viewDonation, name="viewDonation"),
    # path('pay-donation/<int:id>', views.payDonation, name="payDonation"),


    # path('create-public-donation/', views.createPublicDonation, name="createPublicDonation"),
    # path('view-public-donations/', views.viewPublicDonations, name="viewPublicDonations"),
    # path('view-public-donation/<int:id>', views.viewPublicDonation, name="viewPublicDonation"),
    # path('edit-public-donation/<int:id>', views.editPublicDonation, name="editPublicDonation"),
    # path('pay-public-donation/<int:id>', views.payPublicDonation, name="payPublicDonation"),
    # path('public-donors/', views.publicDonors, name="publicDonors"),


    # path('assign-subscribers/', views.assignSubscriber, name="assignSubscriber"),
    # # path('view-subscribers/', views.viewSubscribers, name="viewSubscribers"),
    # path('ajax/unassign_subscriber/', views.unassignSubscriber, name='unassignSubscriber'),
    # path('deactivated/', views.deactivated, name='deactivated'),



    # path('assign-payment/', views.assignPaymentDuration, name="assignPaymentDuration"),
    # path('assign-donation/<int:pk>', views.assignDonation, name="assignDonation"),
    path('assign-payments/<int:pk>', views.assignPaymentsDuration, name="assignPaymentsDuration"),
    path('view-payment-details/', views.viewPaymentDuration, name="viewPaymentDuration"),
    path('delete-invoice/<int:id>', views.deletePaymentDuration, name='deletePaymentDuration'),




    path('ajax/load-groups/', views.load_groups, name='ajax_load_groups'),
    path('ajax/load-code/', views.load_code, name='ajax_load_code'),

    path('ajax/load_bill/', views.load_bill, name='ajax_load_bill'),
    
    path('ajax/load-subgroups/', views.load_subgroups, name='ajax_load_subgroups'),

    path('ajax/load-items/', views.load_items, name='ajax_load_items'),

    path('ajax/load-breakdown/', views.load_breakdown, name='ajax_load_breakdown'),

    path('ajax/load-amount-due/', views.load_amount_due, name='ajax_load_amount_due'),
    path('ajax/load-credit/', views.load_credit, name='ajax_load_credit'),
    path('ajax/load-invoice/', views.load_invoice, name='ajax_load_invoice'),
    path('ajax/load_balance/', views.load_balance, name='ajax_load_balance'),
    path('ajax/load_fee/', views.load_fee, name='ajax_load_fee'),
    path('ajax/delete_payment/', views.delete_payment, name='ajax_delete_payment'),
    path('ajax/delete_assigned/', views.delete_assigned, name='ajax_delete_assigned'),
    path('ajax/delete_invoice/', views.delete_invoice, name='ajax_delete_invoice'),

    # path('ajax/period/', views.period, name='ajax_period'),
    # path('ajax/period/', context_processors.period, name='ajax_period'),
    # path('send-sms/', views.send_sms, name='send_sms'),
    path('send-mail/<int:pk>', views.send_mail, name='send_mail'),
    path('logout/<str:id>/', views.logout, name='logout'),
    path('view-members/', views.viewMembers, name='viewMembers'),
    # path('thank-you/', views.thank_you, name='thank_you'),
    path('activity-log/', views.viewActivityLog, name='viewActivityLog'),

    # path('make-payment/', views.makePayment, name="makePayment"),
    path('make-payments/<int:pk>', views.makePayments, name="makePayments"),
    path('view-assigned/<int:pk>', views.viewAssigned, name="viewAssigned"),
    path('view-payments/', views.viewPayments, name="viewPayments"),
    path('invoice-details-view/<int:pk>', views.invoice_details_view, name="invoice_details_view"),
    path('donors_csv/', views.donors_csv, name="donors_csv"),
    # path('subscribers_csv/', views.subscribers_csv, name="subscribers_csv"),
    path('donation-details-view/<int:pk>', views.donation_details_view, name="donation_details_view"),
    path('view-details/<int:pk>', views.viewDetails, name="viewDetails"),
    path('view-invoices/<int:pk>', views.viewInvoices, name="viewInvoices"),
    path('view-organization/<int:pk>', views.viewOrganizationDetail, name="viewOrganizationDetail"),
    path('profile/', views.viewProfile, name="viewProfile"),
    path('client-profile/<int:id>', views.viewClientProfile, name="viewClientProfile"),


    # path('send-sms/', views.balances, name="balances"),

    # path('create-invoice-it/', views.createInvoiceType, name="createInvoiceType"),
    # path('home/', views.home, name="home"),
]



