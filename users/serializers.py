from rest_framework import serializers
from .models import customer
from django.contrib.auth import get_user_model


User = get_user_model()
class SignUpSerialzer(serializers.Serializer):
    username= serializers.CharField(max_length=255)
    fullName= serializers.CharField(max_length=255)
    number_id= serializers.CharField(max_length=255)
    password1= serializers.CharField(write_only=True)
    password2= serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id' , 'username', 'fullName' ,'number_id', 'password1' , 'password2']
        read_only_fields = ['id']
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('passwords are not equal.')
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError('username already exist')
        if customer.objects.filter(number_id=data.get('number_id')).exists():
            raise serializers.ValidationError('number id already exist.')
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password1')
        name = validated_data.pop('fullName')
        number_id = validated_data.pop('number_id')

        if not all([username , name , number_id]):
            raise serializers.ValidationError('fill all params')

        user =User(
            username = username,
        )
        user.set_password(password)

        user.save()

        customer.objects.create(
            fullName = name,
            number_id = number_id
        )

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']

        user = User.objects.get(username=username)

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('user is not exist')
        if not user.check_password(password):
            raise serializers.ValidationError('password is incorrect')

        return data