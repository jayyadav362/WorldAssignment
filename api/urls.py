from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("otp_verify/<str:mobile>", views.otp_verify, name="otp_verify"),
    path("re_send_otp/<str:mobile>", views.re_send_otp, name="re_send_otp"),
]