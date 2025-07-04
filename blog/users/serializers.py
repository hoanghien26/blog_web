from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.password_validation import validate_password


User=get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only =True,required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model=User
        fields=  ( 'username', 'email', 'password','confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
            
        )
        return user
    
    def validate_username(self,value ):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Tên đăng nhập đã tồn tại")
        return value
    def validate_password(self,value): 
        
        if not re.search(r'[A-Z]', value):  # Có ít nhất 1 chữ hoa
            raise ValidationError("Mật khẩu phải có ít nhất 1 ký tự viết hoa")
    
        if not re.search(r'[0-9]', value):  # Có ít nhất 1 số
            raise ValidationError("Mật khẩu phải có ít nhất 1 số")
        if not re.search(r'[^A-Za-z0-9]',value):
            raise ValidationError("mật khẩu phải có ký tự đặc biệt ")
        return value
    def validate_email(self,value):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, value):
            raise ValidationError("Email không hợp lệ")
        return value
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({"password": "Mật khẩu không khớp."})
        return attrs
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username","email","first_name","last_name")
    
    def update(self,instance,validated_data):
        return super().update(instance,validated_data)
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Tên đăng nhập đã tồn tại")
        return value
    def validate_email(self,value):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, value):
            raise ValidationError("Email không hợp lệ")
        return value
    def validate_phone_number(self,value):
        if re.search(r'[A-Za-z]',value) or re.search(r'[^A-Za-z0-9]',value):
            raise ValidationError("Số điện thoại không hợp lệ")
        if re.match(r'^0',value):
            raise ValidationError("tên điện thoại không hợp lệ")
        return value
   
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'username', 'email', "phone_number",'first_name', 'last_name', 'is_staff')
        read_only_fields = ('id',  'is_staff')

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "New password fields didn't match."})
        return attrs
    
