import django_filters
from django_filters import DateFilter, CharFilter
from superuser.models import AssignPaymentDuration
from .models import *
# from fee_sys.auth import *
# from fee_sys.requests import *


class AssignPaymentDurationFilter(django_filters.FilterSet):
    member = CharFilter(field_name='member', lookup_expr='icontains')
    branch = CharFilter(field_name='branch', lookup_expr='icontains')
    member_category = CharFilter(field_name='member_category', lookup_expr='icontains')
    group = CharFilter(field_name='group', lookup_expr='icontains')
    subgroup = CharFilter(field_name='subgroup', lookup_expr='icontains')
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = AssignPaymentDuration
        fields = ['fee_type']

   

class PaymentsFilter(django_filters.FilterSet):
    member = CharFilter(field_name='member', lookup_expr='icontains')
    branch = CharFilter(field_name='branch', lookup_expr='icontains')
    member_category = CharFilter(field_name='member_category', lookup_expr='icontains')
    group = CharFilter(field_name='group', lookup_expr='icontains')
    subgroup = CharFilter(field_name='subgroup', lookup_expr='icontains')
    # start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    # end_date = DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Payments
        fields = ['fee_type', 'invoice_no']

 
