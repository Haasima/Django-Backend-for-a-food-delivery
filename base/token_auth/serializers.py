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