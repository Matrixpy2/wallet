from rest_framework import serializers
from .models import users
from django.contrib.auth.models import User

class SignUpSerialzer(serializers.ModelSerializer):
    fullName=serializers.CharField(max_length=255)
    number_id=serializers.CharField(max_length=255)
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields='__all__'

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('passwords are not equal.')

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password1')
        fullName = validated_data.pop('fullName')
        number_id = validated_data.po('number_id')

        if not all([username , fullName , number_id]):
            raise serializers.ValidationError('fill all params')

        user =User(
            username = username,
        )
        user.set_password(password)

        user.save()

        users.objects.create(
            username = username,
            fullName = fullName,
            number_id = number_id
        )

        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']

        user = User.objects.get(username=username)

        if not User.objects.filter(user=user).exists():
            raise serializers.ValidationError('user is not exist')
        if not user.check_password(password):
            raise serializers.ValidationError('password is incorrect')

        return data