from django.db import models
from account.models import Account
import random
from django.db.models import F

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Transaction(models.Model):
    transaction_id = models.IntegerField(unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='Category')
    transaction_type = models.CharField(max_length=10)
    comment = models.CharField(max_length=100, null=True, blank=True)
    datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        self.account.save()
        self.datetime = self.datetime.isoformat()

        super().save(*args, **kwargs)

    def generate_transaction_id(self):
        while True:
            transaction_id = random.randint(3000000, 99999999)
            if not Transaction.objects.filter(transaction_id=transaction_id).exists():
                return transaction_id

    def delete(self, *args, **kwargs):
        account = self.account
        if self.transaction_type == 'income':
            account.balance -= self.amount
        elif self.transaction_type == 'spend':
            account.balance += self.amount
        account.save()
        super(Transaction, self).delete(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.transaction_id}"

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
