from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path("", views.dashboard,name="dashboard"),
    path("signup", views.signup, name="signup"),
    path("login", views.logins, name="login"),
    path("logout", views.logouts, name="logout"),
    path("otp_verify/<str:mobile>", views.otp_verify, name="otp_verify"),
    path("re_send_otp/<str:mobile>", views.re_send_otp, name="re_send_otp"),
    path("autosuggest/", views.autosuggest, name="autosuggest"),
    path("display", views.display, name="display"),
    path("country_details/<str:code>", views.country_details, name="country_details"),
]