from django import forms
from order.models import Order
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)









class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        
        # Set default values for customer and amount fields
        self.fields['customer'].disabled = True  # Disable the customer field
        self.fields['total_amount'].disabled = True  # Disable the amount field

        # Set initial values for customer and amount fields
        if 'instance' in kwargs:
            self.fields['customer'].initial = kwargs['instance'].customer.username
            self.fields['total_amount'].initial = kwargs['instance'].total_amount