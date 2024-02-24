from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        fields = ('username', 'email', 'password','password2' )
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return data

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
