from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import LoginSerializer , SignUpSerialzer
# Create your views here.

class SignUpView(APIView):
    def get(self):
        return Request(
            {
                'message' : 'enter fullName , username , number_id , password1 , password2'
            }
        )
