from django.contrib.auth.models import User
from django.db import models
import random
from django.db.models import Sum


class Account(models.Model):
    account_id = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.account_id:
            self.account_id = self.generate_account_id()

        super().save(*args, **kwargs)  # Сохранение модели

    def generate_account_id(self):
        while True:
            account_id = random.randint(300000000, 900000000)
            if not Account.objects.filter(account_id=account_id).exists():
                return account_id

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bank account'
        verbose_name_plural = 'Bank accounts'

