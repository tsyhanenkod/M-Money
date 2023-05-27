from django import forms
from account.models import *
from transaction.models import *

class TransactionFilterForm(forms.Form):
    TRANSACTION_TYPES = [
        ('', 'All'),  # Empty value for selecting all types
        ('income', 'Income'),
        ('spend', 'Expense'),
    ]

    type = forms.ChoiceField(choices=TRANSACTION_TYPES, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='All', required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    account = forms.ModelChoiceField(queryset=Account.objects.all(), empty_label='All', required=False)