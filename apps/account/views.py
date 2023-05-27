from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from transaction.models import *
from account.models import *
from django.db import transaction as db_transaction
from datetime import date, timedelta, datetime
from .forms import *
from django.core.paginator import Paginator
import random
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import JsonResponse

class AccountsView(View):
    def get(self, request):
        user = request.user
        accounts = Account.objects.filter(user=user)
        transactions = Transaction.objects.filter(account__in=accounts).order_by(F('datetime').desc())
        today = datetime.now().date().strftime('%B %d, %Y')
        yesterday = (datetime.now().date() - timedelta(days=1)).strftime('%B %d, %Y')

        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        transactions_by_date = {}
        for transaction in page_obj:
            transaction_date = transaction.datetime.strftime('%B %d, %Y')
            if transaction_date not in transactions_by_date:
                transactions_by_date[transaction_date] = []
            transactions_by_date[transaction_date].insert(0, transaction)

        context = {
            'accounts': accounts,
            'transactions': page_obj,
            'transactions_by_date': transactions_by_date,
            'today': today,
            'yesterday': yesterday,
        }

        return render(request, 'account/accounts.html', context)


class AccountEditView(View):
    def get(self, request, id):
        account = Account.objects.get(id=id)
        context = {
            'account': account,
        }
        return render(request, 'account/account_edit.html', context)

    def post(self, request, id):
        account = Account.objects.get(id=id)

        if 'delete' in request.POST:
            account.delete()
            return redirect('accounts')
        elif 'save' in request.POST:
            account.name = request.POST['name']
            account.balance = request.POST['balance']
            account.save()

        return redirect('accounts')


class PaymentView(View):
    def get(self, request):
        form = PaymentForm(user=request.user)
        context = {
            'form': form,
        }
        return render(request, 'account/payment.html', context)

    def post(self, request):
        form = PaymentForm(request.user, request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            amount = cleaned_data['amount']
            account = cleaned_data['account']
            category = cleaned_data['category']
            payment_trigger = cleaned_data['payment_trigger']

            if payment_trigger == 'income':
                account.balance += amount
            elif payment_trigger == 'spend':
                account.balance -= amount

            account.save()

            date = datetime.combine(cleaned_data['date'], datetime.min.time())
            transaction = Transaction(
                account=account,
                amount=amount,
                category=category,
                transaction_type=payment_trigger,
                comment=cleaned_data['comment'],
                datetime=date
            )

            transaction.save()

            form = PaymentForm(request.user)
            return redirect('accounts')
        else:
            context = {
                'form': form,
            }
            return render(request, 'account/payment.html', context)

    def delete_transaction(request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        transaction.delete()
        return redirect('accounts')



class CreateView(View):
    def get(self, request):
        form = AccountCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'account/create.html', context)

    def post(self, request):
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = Account(
                name=form.cleaned_data['name'],
                balance=form.cleaned_data['balance'],
                user=request.user
            )
            account.save()
            return redirect('accounts')  # Перенаправление после успешного создания аккаунта
        # Обработка недопустимой формы или вывод ошибок
        context = {
            'form': form,
            # Остальной контекст представления...
        }
        return render(request, 'account_creation.html', context)

# class EditAccount(View):
#     def post(self, request):
