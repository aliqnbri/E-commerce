from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from account.models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token
 
 

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', )
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class VerifyAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
