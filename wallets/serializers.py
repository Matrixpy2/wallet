from rest_framework import serializers
from .models import wallets, Transactions, transmission


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = wallets
        fields ='__all__'
class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields =['type' , 'amount' , 'date']
class DepositSerializer(serializers.Serializer):
    amount = serializers.CharField(required=True)
    def validate_amount(self , value):
        value = int(value)
        if value<=0:
            raise serializers.ValidationError('incorrect value')
        return value
class WithdrawSerializer(serializers.Serializer):
    amount = serializers.CharField(required=True)
    def validate_amount(self , value):
        value = int(value)
        if value<=0:
            raise serializers.ValidationError('incorrect value')
        return value

class TransmissionSerializer(serializers.ModelSerializer):
    from_wallet = serializers.HiddenField(default=serializers.CurrentUserDefault())
    amount = serializers.CharField(required=True)
    class Meta:
        model = transmission
        fields = ['from_wallet' , 'to_wallet' , 'amount']
    def validate_amount(self , value):
        value = int(value)
        if value <= 0:
            raise serializers.ValidationError('incorrect value')
        return value

