from django.db import models

# Create your models here.
from django.db import models
from users.models import customer


class wallets(models.Model):
    owner = models.ForeignKey(
        customer,
        on_delete=models.CASCADE,
        verbose_name='کیف پول'
    )
    accont_balance = models.CharField(max_length=255, verbose_name='موجودی حساب')

    def __str__(self):
        return self.accont_balance


class Transactions(models.Model):
    wallet = models.ForeignKey(
        wallets,
        on_delete=models.CASCADE,
        verbose_name='حساب مبدا'
    )
    TRANSACTION_TYPES = (
        ('deposit', 'واریز'),
        ('withdraw', 'برداشت'),
        ('transmission', 'انتقال'),
    )
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPES, verbose_name='نوع تراکنش')
    amount = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'transaction type : {self.type} , amount : {self.amount}'


class transmission(models.Model):
    from_wallet = models.ForeignKey(
        wallets,
        on_delete=models.CASCADE,
        verbose_name='کیف پول مبدا',
        related_name='outgoing_transmissions'
    )
    to_wallet = models.ForeignKey(
        wallets,
        on_delete=models.CASCADE,
        verbose_name='کیف پول مقصد',
        related_name='incoming_transmissions'
    )
    amount = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)

    def __str__(self):
        return f'transfer {self.amount} from {self.from_wallet} to {self.to_wallet}'
