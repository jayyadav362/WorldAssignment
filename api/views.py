from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.serializer import *
import random,string
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


# register new user
@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        serializer = SignUpSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['detail'] = "Register Successfully!"
        else:
            return Response(serializer.errors,status=status.HTTP_409_CONFLICT)
        return Response(data,status=status.HTTP_201_CREATED)


# login step 1
@api_view(['POST'])
def login(request):
    if request.method=='POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            mobile = request.data['mobile']
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
                data['detail'] = 'OTP send to mail successfully.'
                data['mobile'] = mobile
                return Response(data=data,status=status.HTTP_201_CREATED)
            except CustomUser.DoesNotExist:
                data['detail'] = "User with this mobile number does not exist."
                return Response(data=data,status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_409_CONFLICT)


# login step 2
@api_view(['POST'])
def otp_verify(request,mobile):
    if request.method=='POST':
        serializer = OTPSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(phone_number=mobile)
                otp_post = request.data['otp']
                try:
                    otp = OTP.objects.get(otp=otp_post)
                    expire_time = otp.doc+timedelta(minutes=10)
                    if timezone.now() <= expire_time:
                        token, created = Token.objects.get_or_create(user=user)
                        otp.delete()
                        data['token'] = token.key
                        return Response(data=data,status=status.HTTP_201_CREATED)
                    else:
                        data['detail']="OTP has expired."
                        return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
                except OTP.DoesNotExist:
                    data['detail']='Invalid OTP.'
                    return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                data['detail'] =  "User with this mobile number does not exist."
                return Response(data=data,status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
def re_send_otp(request,mobile):
    if request.method=='GET':
        data = {}
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
            data['detail'] = 'OTP send to mail successfully.'
            data['mobile'] = mobile
            return Response(data=data, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            data['detail'] = "User with this mobile number does not exist."
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


# user logout
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'detail':'Logout Successfully!'})
    except (AttributeError, ObjectDoesNotExist):
        return Response({'detail':'AttributeError'},status=status.HTTP_417_EXPECTATION_FAILED)