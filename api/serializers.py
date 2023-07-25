from django.forms import ValidationError
from rest_framework import serializers
from .models import *
from superuser.models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField()
    # token = serializers.CharField()

    def validate_email(self, value):
        if len(value) < 5:
            raise ValidationError("No Jokes please")
        return value 
    
    def validate_password(self, value):
        if value == "":
            raise ValidationError("No Jokes please")
        return value 

    # def tokenise(self):
    #     return self.token


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        if value == "":
            raise ValidationError("This field is required")
        return value         




# class HeroSerializer(serializers.ModelSerializer):
#     description = serializers.SerializerMethodField()

#     class Meta():
#         model = Hero
#         fields = '__all__'

#     def validate_name(self, value):
#         if value == "Joker":
#             raise ValidationError("No Jokes please")
#         return value   

#     def validate(self, data):
#         if len(data["name"]) < 5 or len(data["alias"]) < 5:
#             raise ValidationError("Name should be more than 5")  
#         return data     

#     def get_description(self, data):
#         return "This is " + data.name +"."   






class PaymentSerializer(serializers.Serializer):
    amount_paid = serializers.IntegerField()
    status = serializers.CharField()
    remarks = serializers.CharField()

    def validate_amount_paid(self, value):
        if value == "":
            raise ValidationError("This field is required")
        return value   


class SubscriptionSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    amount_paid = serializers.IntegerField()
    description = serializers.CharField()
    duration = serializers.CharField(required=False)
    renewing_days = serializers.IntegerField()

    def validate_description(self, value):
        if value == "":
            raise ValidationError("This field is required")
        return value   




class FeeTypeSerializer(serializers.ModelSerializer):
    
        class Meta():
            model = FeeType
            fields = ("id", "fee_type")


class FeeDescriptionSerializer(serializers.ModelSerializer):
    
        class Meta():
            model = FeeDescription
            fields = ("id", "fee_description")



class PeriodSerializer(serializers.ModelSerializer):
    
        class Meta():
            model = AssignPeriod
            fields = ("name",)
            


class AssignPaymentDurationSerializer(serializers.ModelSerializer):

    class Meta():
        model = AssignPaymentDuration
        fields = "__all__"



class ClientDetailsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = InvoiceDetails
        fields = "__all__"



class MemberCodeSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Usercode
        fields = "__all__"


class HistorySerializer(serializers.ModelSerializer):
    
    class Meta():
        model = MakePayment
        fields = "__all__"


class PaymentHistorySerializer(serializers.ModelSerializer):

    class Meta():
        model = MakePayment
        fields = (  "client_id",
                    "member_id",
                    "member",
                    "fee_type",
                    "fee_type_value",
                    "fee_description",
                    "fee_description_value",
                    "outstanding_bill",
                    "invoice_type",
                    "assigned_duration",
                    "amount_paid",
                    "payment_status",
                    "arrears",
                    "subscription_expiry",
                    "date_created",
                    )




class PaymentSerializer(serializers.Serializer):

    branch = serializers.CharField(required=False)
    member_category = serializers.CharField(required=False)
    group = serializers.CharField(required=False)
    subgroup = serializers.CharField(required=False)
    member = serializers.CharField(required=False)
    member_id = serializers.CharField(required=False)

    fee_type_id = serializers.CharField(required=False)
    fee_description_id = serializers.CharField(required=False)
    outstanding_bill = serializers.CharField(required=False)
    remarks = serializers.CharField(required=False)
    platform = serializers.CharField(required=False)
    assigned_duration = serializers.CharField(required=False)
    expiration_bill = serializers.CharField(required=False)
    client_id = serializers.CharField(required=False)
    code = serializers.CharField(required=False)

    
    install_range = serializers.CharField(required=False)
    install_period = serializers.CharField(required=False)
    total_amount_due = serializers.CharField(required=False)
    outstanding_balance = serializers.CharField(required=False)
    amount_paid = serializers.CharField(required=False)
    payment_status = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
    arrears = serializers.CharField(required=False)
    invoice_id = serializers.CharField(required=False)
    invoice_type = serializers.CharField(required=False)



    def get_validation_exclusions(self):
        exclusions = super(PaymentSerializer, self).get_validation_exclusions()
        return exclusions + ['end_date', 'install_range', 'payment_status']



class OutstandingBillPaymentSerializer(serializers.Serializer):
    member_id = serializers.CharField()

    def validate_member_id(self, value):
        if value == "":
            raise ValidationError("This field is required")
        return value   


class UsercodeSerializer(serializers.Serializer):
    member_id = serializers.CharField()
    usercode = serializers.CharField()

    def validate_member_id(self, value):
        if value == "":
            raise ValidationError("This field is required")
        return value   




class AutoAssignSerializer(serializers.Serializer):

    branch = serializers.CharField()
    member_category = serializers.CharField()
    group = serializers.CharField()
    subgroup = serializers.CharField()
    member = serializers.CharField()
    member_id = serializers.CharField()
    client_id = serializers.CharField()
    phone = serializers.CharField(required=False)
    email = serializers.EmailField()
    # date_created = serializers.DateField()


    def get_validation_exclusions(self):
        exclusions = super(PaymentSerializer, self).get_validation_exclusions()
        return exclusions + ['phone', 'email', 'member']
