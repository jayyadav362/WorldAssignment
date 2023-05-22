from django.shortcuts import *
from account.forms import *
from django.contrib.auth.decorators import login_required
from account.custom_decorator import *
from django.contrib import messages
import random,string
from django.core.mail import send_mail
from datetime import timedelta
from django.contrib.auth import login,logout
from django.utils import timezone
from itertools import chain
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import F,CharField, Value
# Create your views here.


# register new user
@is_logged_in(redirect_url='account:dashboard')
def signup(request):
    form = SignupForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Register Successfully!")
            return redirect('account:signup')
    data = {
        'form':form
    }
    return render(request,'signup.html',data)


# login step 1
@is_logged_in(redirect_url='account:dashboard')
def logins(request):
    form = LoginForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            mobile = request.POST['mobile']
            try:
                user = CustomUser.objects.get(phone_number=mobile)
                otp = ''.join(random.choices(string.digits, k=6))
                try:
                    get_otp = OTP.objects.get(user=user)
                    get_otp.otp = otp
                    get_otp.doc = timezone.now()
                    get_otp.save()
                except OTP.DoesNotExist:
                    create_otp = OTP.objects.create(user=user,otp=otp, doc=timezone.now())

                # send mail
                subject = "Your One-Time Password (OTP) for Account Verification"
                message = f"Dear {user.first_name} {user.last_name},\n\nTo ensure the security of your account,we are providing you with a One-Time Password (OTP) to complete your account verification.\nYour OTP is: {otp}\nPlease use the above OTP to verify your account within the next 10 minutes. Do not share this OTP with anyone, as it is confidential and will grant access to your account. If you did not request this OTP or are experiencing any issues, please contact our support team immediately.\n\nOnce you have entered the OTP, your account will be successfully verified, and you can start enjoying the benefits of our platform."
                sender = 'mailuser3008@gmail.com'
                send_mail(subject, message, sender, [user.email], fail_silently=False)
                messages.success(request, 'OTP send to mail successfully.')
                return redirect('account:otp_verify',mobile=mobile)
            except CustomUser.DoesNotExist:
                messages.error(request, "User with this mobile number does not exist.")
                return redirect('account:login')
    data = {
        'form': form
    }
    return render(request,'login.html',data)


# login step 2
@is_logged_in(redirect_url='account:dashboard')
def otp_verify(request,mobile):
    form = OTPForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            try:
                user = CustomUser.objects.get(phone_number=mobile)
                otp_post = request.POST['otp']
                try:
                    otp = OTP.objects.get(otp=otp_post)
                    expire_time = otp.doc+timedelta(minutes=10)
                    if timezone.now() <= expire_time:
                        login(request,user)
                        otp.delete()
                        return redirect('account:dashboard')
                    else:
                        messages.error(request, "OTP has expired.")
                        return redirect('account:otp_verify',mobile=mobile)
                except OTP.DoesNotExist:
                    messages.error(request,'Invalid OTP.')
                    return redirect('account:otp_verify',mobile=mobile)
            except CustomUser.DoesNotExist:
                messages.error(request, "User with this mobile number does not exist.")
                return redirect('account:login')
    data = {
        'form': form,
        'mobile':mobile
    }
    return render(request,'otp_verify.html',data)


@is_logged_in(redirect_url='account:dashboard')
def re_send_otp(request,mobile):
    try:
        user = CustomUser.objects.get(phone_number=mobile)
        otp = ''.join(random.choices(string.digits, k=6))
        try:
            get_otp = OTP.objects.get(user=user)
            get_otp.otp = otp
            get_otp.doc = timezone.now()
            get_otp.save()
        except OTP.DoesNotExist:
            create_otp = OTP.objects.create(user=user, otp=otp, doc=timezone.now())

        # send mail
        subject = "Your One-Time Password (OTP) for Account Verification"
        message = f"Dear {user.first_name} {user.last_name},\n\nTo ensure the security of your account,we are providing you with a One-Time Password (OTP) to complete your account verification.\nYour OTP is: {otp}\nPlease use the above OTP to verify your account within the next 10 minutes. Do not share this OTP with anyone, as it is confidential and will grant access to your account. If you did not request this OTP or are experiencing any issues, please contact our support team immediately.\n\nOnce you have entered the OTP, your account will be successfully verified, and you can start enjoying the benefits of our platform."
        sender = 'mailuser3008@gmail.com'
        send_mail(subject, message, sender, [user.email], fail_silently=False)
        messages.success(request, 'OTP send to mail successfully.')
        return redirect('account:otp_verify', mobile=mobile)
    except CustomUser.DoesNotExist:
        messages.error(request, "User with this mobile number does not exist.")
        return redirect('account:login')


@login_required(login_url='account:login')
def logouts(r):
    logout(r)
    return redirect('account:login')


def autosuggest(request):
    search = request.GET.get('search', None)
    results = []
    if search is not None:
        city = City.objects.filter(name__istartswith=search).values('name').annotate(type=Value('city',output_field=CharField()))
        country = Country.objects.filter(name__istartswith=search).values('name','code').annotate(type=Value('country',output_field=CharField()))
        language = Countrylanguage.objects.filter(language__istartswith=search).values(name=F('language')).annotate(type=Value('language',output_field=CharField()))
        results = chain(city, country, language)
    return JsonResponse(list(results), safe=False)


@login_required(login_url='account:login')
def dashboard(request):
    return render(request,'dashboard.html')


@login_required(login_url='account:login')
def display(request):
    search = request.GET.get('search', None)
    if search:
        city = City.objects.select_related('countrycode').filter(name__istartswith=search)
        country = Country.objects.filter(name__istartswith=search)
        language = Countrylanguage.objects.select_related('countrycode').filter(language__istartswith=search)
        search_results = chain(city, country, language)
    else:
        search_results = []
    paginator = Paginator(list(search_results), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'page_obj':page_obj,
        'search':search,
        'count':len(page_obj)
    }
    return render(request,'display.html',data)


@login_required(login_url='account:login')
def country_details(request,code):
    try:
        country = Country.objects.get(code=code)
    except Country.DoesNotExist:
        country = None
    data = {
        'country':country
    }
    return render(request,'country_details.html',data)