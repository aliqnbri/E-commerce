from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from account.models import CustomUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email

        return token




class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'password', 'password2' )
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_phone_number(self,value):
        qs = CustomUser.objects.filter(phone_number__exact=value) or CustomUser.objects.filter(email__exact=value)
        if qs.exists():
            raise serializers.ValidationError(f"{value} is already exist")


    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from the validated data
        user = CustomUser.objects._create_user(**validated_data)
        return user    
    
    def update (self,instance,validated_data):
        validated_data.pop('password2')  # Remove password2 from the validated data
        instance.email = validated_data.get('email')
        instance.password = validated_data.get('password')
        instance.phone_number = validated_data.get('phone_number')

        return instance



class VerifyAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
