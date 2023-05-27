from django import forms
from .models import Account
from transaction.models import *
import random
from decimal import Decimal


class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    comment = forms.CharField(max_length=100, required=False)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    account = forms.ModelChoiceField(queryset=None, empty_label='--- Account ---')
    payment_trigger = forms.ChoiceField(widget=forms.RadioSelect, choices=[('income', 'Income'), ('spend', 'Spend')])
    category = forms.ModelChoiceField(queryset=None, empty_label='--- Category ---')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)
        self.fields['category'].queryset = Category.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get('comment')
        if comment == '':
            cleaned_data['comment'] = None
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get('comment')
        if comment == '':
            cleaned_data['comment'] = None
        return cleaned_data

    def save(self):
        transaction = Transaction(
            amount=self.cleaned_data['amount'],
            comment=self.cleaned_data['comment'],
            date=self.cleaned_data['date'],
            account=self.cleaned_data['account'],
            category=self.cleaned_data['category'],
            payment_trigger=self.cleaned_data['payment_trigger'],
        )
        transaction.transaction_id = self.generate_transaction_id()

        transaction.save()
        return transaction

class AccountCreationForm(forms.Form):
    name = forms.CharField(max_length=50)
    balance = forms.DecimalField(max_digits=10, decimal_places=2)
