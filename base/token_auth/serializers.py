from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from address.models import UserAddress, Country, City
from address.serializers import UserAddressSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'address')
        
        
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        if phone and password:
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                raise serializers.ValidationError('Wrong phone or password')
            
            if not user.check_password(password):
                raise serializers.ValidationError('Wrong phone or password')
            
            if not user.is_active:
                raise serializers.ValidationError('This account is not active')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include "phone" and "password"')
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password')
        
    def validate(self, attrs):
        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError('User with this phone number is already exists')
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('User with this email is already exists')
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user