from django.urls import path
from .views import LogInApi , SignUpApi


urlpatterns = [
    path('signup' , SignUpApi.as_view() , name='signup_user'),
    path('login'  , LogInApi.as_view()   , name='login_user'),
]