import datetime
from email.policy import default
from time import timezone

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import wallets , Transactions , transmission
from .serializers import WalletSerializer , TransactionsSerializer
from rest_framework import status

class MywalletsApi(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer
    queryset = wallets.objects.all()
    def get_queryset(self):
        return wallets.objects.filter(owner = self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def list(self , request):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    'message' : 'هیچ کیف پولی ندارید'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(queryset , many = True)
        return Response(
            {
            'your wallets': serializer.data,
            'check transactions': '/wallets/{wallet id}/transactions/'
            },
            status=status.HTTP_200_OK
        )


    @action(detail=True , methods=['get'] , url_path='transactions')
    def get_transactions(self , requst , pk=None):
        wallet = get_object_or_404(wallets , id=pk)



        if wallet.owner != requst.user:
            return Response(
                {
                    'message' : 'شما کیف پولی با این شناسه ندارید'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        transactions = Transactions.objects.filter(wallet=wallet).order_by('-date')
        serializer = TransactionsSerializer(transactions, many=True)

        return Response(
            {
            'Transactions': serializer.data,
            'wallet_id': wallet.id,
            'balance': wallet.accont_balance
        },
            status=status.HTTP_200_OK
        )
    @action(detail=True , methods=['post'] , url_path='transmission')
    def transfer(self , request ,pk = None):
        from_wallet = self.get_object()
        to_wallet = request.data.get('to_wallet')
        amount = request.data.get('amount')

        # Check params

        if not to_wallet:
            return Response(
                {
                    'message' : 'کیف پول مقصد را مشخص کنید'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if not amount:
            return Response(
                {
                    'message' : 'مقداری که میخواهید انتقال دهید را مشخص کنید'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        # Check balance
        current_balance = int(from_wallet.accont_balance)
        namount = int(amount)
        if namount > current_balance:
            return Response(
                {
                    'message' : 'موجودی کافی نیست'
                },status=status.HTTP_400_BAD_REQUEST
            )
        try:
            to_wallet = wallets.objects.get(id=to_wallet)
        except wallets.DoesNotExist:
            return Response(
                {'error': 'کیف پول مقصد وجود ندارد'},
                status=status.HTTP_404_NOT_FOUND
            )

        #transfering

        new_from_balance = current_balance - namount
        from_wallet.accont_balance = str(new_from_balance)
        from_wallet.save()

        new_to_balance = current_balance + namount
        to_wallet.accont_balance = str(new_to_balance)
        to_wallet.save()

        transaction_from = Transactions.objects.create(
            wallet = from_wallet,
            type='transmission',
            amount = f'-{amount}'
        )
        transaction_to =Transactions.objects.create(
            wallet = from_wallet,
            type='transmission',
            amount = amount
        )
        transmission.objects.create(
            from_wallet=from_wallet,
            to_wallet = to_wallet,
            amount = amount,
        )

        return Response(
            {
                'message' : 'انتقال با موفقیت انجام شد',
                'transmission' : f'transfer {amount} from {from_wallet.id} to {to_wallet.id}'
            },status=status.HTTP_200_OK
        )

    @action(detail=True , methods=['post'] , url_path='deposit')
    def Deposit(self , request , pk=None):
        wallet = self.get_object()
        amount = request.data.get('amount')
        if not amount:
            return Response(
                {
                    'message' : 'مقدار واریزی را وارد کنید'
                },status=status.HTTP_400_BAD_REQUEST
            )
        current_balance =int(wallet.accont_balance)
        new_balance = current_balance + int(amount)
        wallet.accont_balance = str(new_balance)
        wallet.save()
        Transactions.objects.create(
            wallet = wallet,
            type = 'deposit',
            amount = amount
        )

        return Response(
            {
                'message' : 'واریز با موفقیت انجام شد',
                'amount' : amount,
            },status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='withdraw')
    def withdraw(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get('amount')
        if not amount:
            return Response(
                {
                    'message': 'مقدار واریزی را وارد کنید'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        current_balance = int(wallet.accont_balance)

        if current_balance<int(amount):
            return Response(
                {
                    'message' : 'موجودی کافی نیست'
                },status=status.HTTP_403_FORBIDDEN
            )
        new_balance = current_balance - int(amount)
        wallet.accont_balance = str(new_balance)
        wallet.save()
        Transactions.objects.create(
            wallet=wallet,
            type='withdraw',
            amount=f'-{amount}'
        )

        return Response(
            {
                'message': 'برداشت با موفقیت انجام شد',
                'amount': amount,
            }, status=status.HTTP_200_OK
        )



