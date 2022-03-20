from django import forms
from subscription.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("name", "price", "billingPeriod", "stripeProductId")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'billingPeriod': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'stripeProductId': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'name': 'Product Name',
            'price': 'Product Price',
            'billingPeriod': 'Product Billing Period',
            'stripeProductId': 'Product Stripe Id',
        }
        help_texts = {
            'name': 'Eg : Standard Plan',
            'price': 'Eg : 250 (As per given on stripe)',
            'billingPeriod': 'Eg : Monthly / Quarterly / Yearly',
            'stripeProductId': 'Eg : price_1Kcwxxxxxxxxxxxxxxxxxxxx (As per given on stripe)',
        }
