from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .models import Profile
import random
import http.client
from twilio.rest import Client
from django.conf import settings
from django.contrib.auth import authenticate, login

def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    # conn = http.client.HTTPSConnection("api.msg91.com")
    # authkey = settings.AUTH_KEY 
    # headers = { 'content-type': "application/json" }
    # url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    # conn.request("GET", url , headers=headers)
    # res = conn.getresponse()aa4ccf337fdb4046883b3f8cea22ceef
    account_sid = 'AC827982c02d08b4edbee729020831fb1a'
    auth_token = 'a7c973ea6c9d1d73ff3ee4ee19caf6df'
    body = 'Hello your otp is here'+str(otp)
 
    client = Client(account_sid, auth_token)
    print("Sending '%s' to %s" % (body, mobile))
 
    message = client.messages.create(
                              from_='+12563877197',
                              body =body,
                              to =str(mobile)
                          )
    print(message.sid)
    # data = res.read()
    # print(data)
    return None
def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            user = User.objects.get(id = profile.user.id)
            login(request , user)
            return redirect('cart')
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'login_otp.html' , context)
    
    return render(request,'login_otp.html' , context)
def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        user = Profile.objects.filter(mobile = mobile).first()
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'login.html' , context)
        otp = str(random.randint(1000 , 9999))
        user.otp = otp
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')        
    return render(request,'login.html')
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        if check_user or check_profile:
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'register.html' , context)
        user = User(email = email , first_name = name, username=name)
        user.save()
        otp = str(random.randint(1000 , 9999))
        profile = Profile(user = user , mobile=mobile , otp = otp) 
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request,'register.html')
def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            return redirect('cart')
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'otp.html' , context)
            
        
    return render(request,'otp.html' , context)
def cart(request):
    return render(request, 'cart.html')