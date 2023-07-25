from django.urls import include, path, re_path
# from api import context_processors
from rest_framework import routers
from . import views
from . import context_processors

# router = routers.DefaultRouter()
# # router.register(r'heroes', views.HeroViewSet)
# # router.register(r'villains', views.VillainViewSet)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Fee Manager API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   #  path('login/', views.Login.as_view(), name="login"),
    path('member-total/<str:member_id>/', views.GetMemberTotal.as_view(), name="member_total"),
    path('client-total/<str:client_id>/', views.GetClientTotal.as_view(), name="client_total"),
    path('fee-types/<str:client_id>/', views.GetFeeTypes.as_view(), name="fee_types"),
    path('fee-descriptions/<str:client_id>/', views.GetFeeDescriptions.as_view(), name="fee_descriptions"),
    path('periods/', views.GetPeriods.as_view(), name="periods"),

    path('amount-due/id=<str:id>/range=<str:range>/period=<str:period>/', views.GetAmountDue.as_view(), name="load_amount_due"),
    path('credit/member_id=<str:member_id>/', views.GetCredit.as_view(), name="load_credit"),
    path('payment-link/', views.GetPaymentLink.as_view(), name="payment_link"),


    path('pay-outstanding-bill/', views.PayOutstandingBill.as_view(), name="pay_outstanding_bill"),


    path('dashboard/<str:token>/', views.Dashboard.as_view(), name="dashboard"),
    path('make-payment/token=<str:token>/', views.AssignedFees.as_view(), name="make_payment"),


    
    path('payment-history/', views.GetPaymentHistory.as_view(), name="payment_history"),
    path('history/<str:mid>/<str:pid>/', views.GetHistory.as_view(), name="history"),

    path('account-expiry/<str:member_id>/', views.GetAccountExpiry.as_view(), name="account_expiry"),


    path('outstanding-bill/<str:member_id>/', views.GetOutstandingBill.as_view(), name="outstanding_bill"),
    path('send-payment-mail/<str:member_id>/', views.SendPaymentMail.as_view(), name="send_payment_mail"),


    path('assigned-fees/<str:usercode>/<str:client_id>/', views.GetAssignedFeesByCode.as_view(), name="assigned_fees_by_code"),
   #  path('assigned-fees/<str:member_id>/<str:client_id>/', views.GetAssignedFeesByMid.as_view(), name="assigned_fees_by_mid"),

    path('validate-code/<str:usercode>/', views.ValidateCode.as_view(), name="validate_code"),
    
    path('auto-assign/', views.AutoAssign.as_view(), name="auto_assign"),
    path('update-usercode/', views.UpdateUserCode.as_view(), name="update_usercode"),


    path('assigned-fees-by-id/<str:aid>/', views.GetAssignedFeesById.as_view(), name="assigned_fees_by_id"),
    path('assigned-fees/', views.GetAssignedFees.as_view(), name="assigned_fees"),
    path('member-details/<str:usercode>/', views.GetMember.as_view(), name="code_details"),
    path('base-currency/<str:client_id>/', views.GetBaseCurrency.as_view(), name="base_currency"),
    path('client-details/<str:client_id>/', views.GetClientDetails.as_view(), name="client_details"),
    path('clients/<str:usercode>/', views.GetClients.as_view(), name="clients"),
    path('invoice-breakdown/<str:assigned_id>/', views.GetBreakdown.as_view(), name="invoice_breakdown"),
   #  path('new-history/<str:member_id>/', views.GetNewHistory.as_view(), name="new_history"),



   #  path('make-payment/<int:id>/', views.MakeFeePayment.as_view(), name="pay_fee"),
   #  path('renew-subscription/', views.MakeSubscriptionPayment.as_view(), name="pay_subs"),


   #  path('subscribers/<str:client_id>/', views.GetSubscribers.as_view(), name="subs"),


    re_path('swagger', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('assigned-fees/token', views.GetAssignedFees.as_view({'post':'post_token'})),
    

    # path('total-paid/', views.TotalPaid.as_view(), name="total_paid"),

    # path('list/<int:pk>', views.HeroDetails.as_view(), name="heros"),
    # path('members/', views.members, name="members"),
]