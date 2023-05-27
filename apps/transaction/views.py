from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from transaction.models import *
from account.models import *
from django.urls import reverse
from datetime import date, timedelta, datetime
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from account.forms import *
from .forms import *





class HistoryView(View):
    def get(self, request):
        user = request.user
        accounts = Account.objects.filter(user=user)

        filter_form = TransactionFilterForm(request.GET)

        if filter_form.is_valid():
            filters = {}
            transaction_type = filter_form.cleaned_data['type']
            category = filter_form.cleaned_data['category']
            start_date = filter_form.cleaned_data['start_date']
            end_date = filter_form.cleaned_data['end_date']
            account = filter_form.cleaned_data['account']

            if transaction_type:
                filters['transaction_type'] = transaction_type
            if category:
                filters['category'] = category
            if start_date and end_date:
                filters['datetime__range'] = (start_date, end_date)
            if account:
                filters['account'] = account

            transactions = Transaction.objects.filter(account__in=accounts, **filters).order_by('-datetime')
        else:
            transactions = Transaction.objects.filter(account__in=accounts).order_by('-datetime')

        if transactions.exists():
            first_transaction_date = transactions.last().datetime.date()
            last_transaction_date = transactions.first().datetime.date()
        else:
            first_transaction_date = last_transaction_date = timezone.now().date()

        total_income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total']
        total_expense = transactions.filter(transaction_type='spend').aggregate(total=Sum('amount'))['total']
        total_income = total_income or 0
        total_expense = total_expense or 0

        if start_date and end_date:
            num_days = (end_date - start_date).days + 1
            average_income_per_day = total_income / num_days
            average_expense_per_day = total_expense / num_days
        else:
            num_days = (last_transaction_date - first_transaction_date).days + 1
            average_income_per_day = total_income / num_days
            average_expense_per_day = total_expense / num_days

        paginator = Paginator(transactions, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        transactions_by_date = {}
        for transaction in page_obj:
            transaction_date = transaction.datetime.strftime('%B %d, %Y')
            if transaction_date not in transactions_by_date:
                transactions_by_date[transaction_date] = []
            transactions_by_date[transaction_date].append(transaction)

        context = {
            'accounts': accounts,
            'transactions': page_obj,
            'transactions_by_date': transactions_by_date,
            'today': timezone.now().date(),
            'yesterday': timezone.now().date() - timedelta(days=1),
            'total_income': total_income,
            'total_expense': total_expense,
            'average_income_per_day': '{:.2f}'.format(average_income_per_day),
            'average_expense_per_day': '{:.2f}'.format(average_expense_per_day),
            'filter_form': filter_form,
        }

        return render(request, 'transactions/transactions_list.html', context)


class DeleteTransaction(DeleteView):
    model = Transaction

    success_url = reverse_lazy('accounts')

    def get_object(self, queryset=None):
        transaction_id = self.kwargs.get('transaction_id')
        return get_object_or_404(Transaction, id=transaction_id)


class EditTransaction(View):
    def get(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        form = PaymentForm(request.user, initial={
            'amount': transaction.amount,
            'comment': transaction.comment,
            'category': transaction.category,
            'account': transaction.account,
            'payment_trigger': transaction.transaction_type,
            'date': transaction.datetime.date()
        })
        return render(request, 'account/payment_edit.html', {'form': form, 'transaction_id': transaction_id})

    def post(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        form = PaymentForm(request.user, request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            amount = cleaned_data['amount']
            account = cleaned_data['account']
            category = cleaned_data['category']
            payment_trigger = cleaned_data['payment_trigger']

            current_balance = account.balance
            current_amount = transaction.amount

            if transaction.transaction_type == 'income':
                if payment_trigger == 'spend':
                    account.balance -= current_amount  # Вычитаем текущую сумму дохода
                    account.balance -= amount  # Вычитаем новую сумму расхода
                elif current_amount != amount:
                    account.balance += amount - current_amount  # Добавляем разницу между текущей и новой суммой

            elif transaction.transaction_type == 'spend':
                if payment_trigger == 'income':
                    account.balance += current_amount  # Добавляем текущую сумму расхода
                    account.balance += amount  # Добавляем новую сумму дохода
                elif current_amount != amount:
                    account.balance += amount - current_amount  # Добавляем разницу между текущей и новой суммой

            account.save()

            # Обновление данных существующей транзакции
            transaction.amount = amount
            transaction.category = category
            transaction.transaction_type = payment_trigger
            transaction.comment = cleaned_data['comment']
            # Не изменять дату и время при редактировании
            transaction.save(update_fields=['amount', 'category', 'transaction_type', 'comment'])

            # Получаем номер текущей страницы из параметров запроса
            page_number = request.GET.get('page')
            return redirect(reverse('accounts') + f'?page={page_number}')
        else:
            context = {
                'form': form,
                'transaction_id': transaction_id
            }
            return render(request, 'account/payment_edit.html', context)










