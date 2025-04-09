from django.urls import path
from . import views
app_name = 'yyauth'

urlpatterns =[
    path('login',views.yylogin,name='login'),
    path('logout',views.yylogout,name='logout'),
    path('register',views.register,name='register'),
    path('captcha',views.send_email_captcha,name='email_captcha'),
]