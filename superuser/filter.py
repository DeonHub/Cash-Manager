import django_filters
from django_filters import DateFilter, CharFilter
from .models import *
# from fee_sys.auth import *
# from fee_sys.requests import *



class InvoicesFilter(django_filters.FilterSet):
    branch = CharFilter(field_name='branch', lookup_expr='icontains')
    member_category = CharFilter(field_name='member_category', lookup_expr='icontains')
    group = CharFilter(field_name='group', lookup_expr='icontains')
    subgroup = CharFilter(field_name='subgroup', lookup_expr='icontains')
    invoice_type = CharFilter(field_name='invoice_type', lookup_expr='icontains')

    class Meta:
        model = Invoice
        fields = ['fee_type']
        

   




class AssignPaymentDurationFilter(django_filters.FilterSet):
    branch = CharFilter(field_name='branch', lookup_expr='icontains')
    member_category = CharFilter(field_name='member_category', lookup_expr='icontains')
    group = CharFilter(field_name='group', lookup_expr='icontains')
    subgroup = CharFilter(field_name='subgroup', lookup_expr='icontains')
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')


    class Meta:
        model = AssignPaymentDuration
        fields = ['fee_type']
        

   




class PaymentsFilter(django_filters.FilterSet):
    branch = CharFilter(field_name='branch', lookup_expr='icontains')
    member_category = CharFilter(field_name='member_category', lookup_expr='icontains')
    group = CharFilter(field_name='group', lookup_expr='icontains')
    subgroup = CharFilter(field_name='subgroup', lookup_expr='icontains')
    invoice_type = CharFilter(field_name='invoice_type', lookup_expr='icontains')
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = MakePayment
        fields = ['fee_type']

 


class ActivitiesFilter(django_filters.FilterSet):
    branch = CharFilter(field_name='branch', lookup_expr='icontains')
    user = CharFilter(field_name='user', lookup_expr='icontains')

    class Meta:
        model = ActivityLog
        fields = ['client_id']




# class MembersFilter(django_filters.FilterSet):
#     member = CharFilter(field_name='member', lookup_expr='icontains')

#     class Meta:
#         model = Members
#         fields = ['branch']


# class SubscribersFilter(django_filters.FilterSet):
#     member = CharFilter(field_name='member', lookup_expr='icontains')

#     class Meta:
#         model = Members
#         fields = ['branch']


# class SubscribersFilter(django_filters.FilterSet):
#     member = CharFilter(field_name='member', lookup_expr='icontains')
#     member_category = CharFilter(field_name='member_category', lookup_expr='icontains')
#     group = CharFilter(field_name='group', lookup_expr='icontains')
#     subgroup = CharFilter(field_name='subgroup', lookup_expr='icontains')

#     class Meta:
#         model = Members
#         fields = ['branch']

   
