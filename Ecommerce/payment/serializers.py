from rest_framework import serializers
from account.models import CustomerProfile# Assuming User model from django.contrib.auth

class PaymentSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='CustomerProfile.username')  # Read-only username
    status_display = serializers.CharField(source='get_status_display')  # Human-readable status

    class Meta:
        model = Payment
        fields = ('id', 'user_username', 'order', 'amount', 'status', 'status_display')
        validators = [
            serializers.UniqueTogetherValidator(queryset=Payment.objects.all(), fields=('user', 'order')),
        ]

    def validate(self, data):
        # Combine custom validation with serializer validation
        if data['amount'] < Decimal('0.00'):
            raise serializers.ValidationError('Amount cannot be negative.')
        return data
