from rest_framework import serializers
from django.contrib.auth.models import User
from .models import HrTeam, EmployeeDetails, Customer,NewTable

class EmployeeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrTeam
        fields = "__all__"

class EmployeeDetailsSerializer(serializers.ModelSerializer):
    # Uncomment and configure if password handling is needed in the future
    # password = serializers.CharField(
    #     style={'input_type': 'password'},
    #     write_only=True, allow_null=True, allow_blank=True
    # )

    class Meta:
        model = EmployeeDetails
        fields = '__all__'

    # Example create method if custom user creation is needed
    # def create(self, validated_data):
    #     data = validated_data
    #     password = str(data.pop("password"))
    #     data['username'] = data['username'].lower()
    #     user = User.objects.create(**data)
    #     user.set_password(password)
    #     user.save()
    #     return user

class CustomerSerializer(serializers.ModelSerializer):
    # Uncomment and configure if password handling is needed in the future
    # password = serializers.CharField(
    #     style={'input_type': 'password'},
    #     write_only=True, allow_null=True, allow_blank=True
    # )

    class Meta:
        model = Customer
        fields = '__all__'

class PDFGenerationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    designation = serializers.CharField(max_length=100)
    ctc = serializers.IntegerField()
    description = serializers.CharField(max_length = 1000)
    # Add more fields as needed


class ColumnCreationSerializer(serializers.Serializer):
    column_name = serializers.CharField(max_length=100)
    data_type = serializers.CharField(max_length=100)
    # table_name = serializers.CharField(max_length=100)  # Assuming you'll also provide the table name



