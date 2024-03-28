from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from account.models import CustomUser , Address ,CustomerProfile
from django.contrib.auth import authenticate


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['phone_number'] = user.phone_number

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'password', 'password2')

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
                raise serializers.ValidationError(
                    {'password': 'Passwords do not match.'})    

    
        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists.' if email else 'Phone number already exists.'})

        

        return attrs

    def create(self, validated_data):
    
        validated_data.pop('password2')
        user = CustomUser.objects._create_user(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
 
        validated_data.pop('password2')
        instance.email = validated_data.get('email')
        instance.password = validated_data.get('password')
        instance.phone_number = validated_data.get('phone_number')

        return instance




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            self.context['request'], email=email, password=password)

        if user is not None:
            self.context['user'] = user
            return attrs

        raise serializers.ValidationError('Invalid email or password.')



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street', 'city', 'postal_code', 'detail')




class CustomerProfileSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)  # Human-readable gender
    username = serializers.ReadOnlyField()  # Read-only username from related User
    address = AddressSerializer(read_only=True)  # Nested read-only address

    class Meta:
        model = CustomerProfile
        fields = ('id', 'first_name', 'last_name', 'gender', 'gender_display', 'username', 'avatar', 'address')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.avatar:
            representation['avatar'] = instance.avatar.url  # Provide absolute URL for avatar
        
        return representation

