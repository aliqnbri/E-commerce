from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from account.models import CustomUser, CustomerProfile
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from product.models import Category , Product , Review
from coupon.models import Coupon
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email


        return token
 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username','email','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data ):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)   
        instance.save()
        return instance    



class VerifyAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class LoginSerailizer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'        


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'        




class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'product', 'code', 'discount_percent', 'discount_amount', 'expiration_date', 'valid_from', 'is_active']

    def calculate_discounted_price(self, obj):
        if obj.discount_percent is not None:
            return obj.product.price * (1 - (obj.discount_percent / 100))
        elif obj.discount_amount is not None:
            return obj.product.price - obj.discount_amount
        else:
            return obj.product.price        