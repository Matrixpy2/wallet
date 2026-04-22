from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer , SignUpSerialzer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
# Create your views here.

class SignUpApi(APIView):
    def get(self , request):
        return Response(
            {
                'message' : 'enter fullName , username , number_id , password1 , password2'
            },
            status=status.HTTP_200_OK
        )
    def post(self ,request):
        data = request.data
        print(data)
        ser = SignUpSerialzer(data=data)
        print(ser)
        if ser.is_valid():
            print('ser is valid')
            data = ser.validated_data
            user = ser.save()
            return Response(
                {
                    'message': f"{data['username']} Created."
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'error':f'{ser.errors}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class LogInApi(APIView):
    def get(self , request):
        return Response(
            {
                'message' : "enter username and password"
            },
            status=status.HTTP_200_OK
        )
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        if ser.is_valid():
            username = ser.validated_data['username']
            user = User.objects.get(username=username)

            token = RefreshToken.for_user(user=user)
            return Response(
                {
                    'message' : f'you are logged in with {username} username',
                    'token' : str(token)
                },
                status=status.HTTP_200_OK
            )

