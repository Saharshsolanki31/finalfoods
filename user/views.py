from django.shortcuts import render

# Create your views here.
import random
from datetime import datetime
import random
import string

from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template

from food import settings
from restaurant.models import restaurant
from user.models import user, BookTable


def home(request):
    if 'user_email' in request.session:
        return render(request,'user/home.html')
    else:
        return redirect(login)


def user_profile(request):
    if 'user_email' in request.session:
        profile_data=user.objects.get(email=request.session['user_email'])
        print(profile_data.image)
        return render(request,'user/user_profile.html',{"profile_data":profile_data})
    else:
        return redirect(login)

def update_user_profile(request):
    if 'user_email' in request.session:
        if 'phone' in request.POST:
            profile_data = user.objects.get(email=request.session['user_email'])
            profile_data.phone=request.POST['phone']
            profile_data.save()
        if 'password' in request.POST:
            profile_data = user.objects.get(email=request.session['user_email'])
            profile_data.password = request.POST['password']
            profile_data.save()
        if 'image' in request.FILES:
            profile_data = user.objects.get(email=request.session['user_email'])
            profile_data.image = request.FILES['image']
            profile_data.save()

        return redirect(user_profile)
    else:
        return redirect(login)

# function for book table
def book_table(request,id):
    if 'user_email' in request.session:
        user_data=user.objects.get(email=request.session['user_email'])
        obj=user_data.id
        booking_details=BookTable.objects.filter(user_email=obj).order_by('-id')
        if request.method=="POST":
            user_name=request.POST['user_name']
            user_contact=request.POST['user_contact']
            user_email=request.POST['user_email']
            date=request.POST['date']
            time=request.POST['time']
            data=restaurant.objects.get(id=id)
            restaurant_name=data.restaurant_name
            guests=request.POST['guests']
            table=BookTable(user_name=user_name,rest_id=id,restaurant_name=restaurant_name,user_email=user.objects.get(email=request.session['user_email']),user_contact=user_contact,date=date,time=time,guests=guests)
            table.save()
            messages.warning(request,"Your table is in pending status, wait for confirmation")
            return redirect(book_table,id=id)

        return render(request,'user/book_table.html',{"user_data":user_data,"booking_details":booking_details,"id":id})
    else:
        return redirect(login)

# cancel booked table
def cancel_booking(request,id):
    if 'user_email' in request.session:
        booking_details=BookTable.objects.get(id=id)
        booking_details.status="cancel"
        rest_id=booking_details.rest_id
        booking_details.save()
        messages.success(request,"Booking cancel")
        return redirect(book_table,id=rest_id)


    else:
        return redirect(login)


# login function
def login(request):
    if 'user_email' in request.session:
        return redirect(home)
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            if user.objects.filter(email=email).exists():
                if user.objects.filter(email=email, password=password).exists():
                    msg = "Login-In Successfuly!! "
                    my_user = user.objects.get(email=email)
                    request.session['user_email'] = email
                    messages.success(request,msg)
                    return redirect(home)
                else:
                    msg = "Inccorect Password !"
                    messages.success(request, msg)
                    return redirect(login)
            else:
                msg = "Email is Not Registered !"
                messages.error(request, msg)
                return redirect(register)
        else:
          return render(request, "user/login.html")







def register(request):
    if request.method=="POST":
        email=request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        if user.objects.filter(email=email).exists():
            msg="You have Already Registered !"
            messages.success(request,msg)
            return redirect(register)
        elif user.objects.filter(phone=phone).exists():
            msg = "Mobile Number is linked With Another Account !"
            messages.success(request, msg)
            return redirect(register)
        else:
            otp=random.randint(1000,9999)
            subject = "ONE TIME PASSWORD VERIFCTAION CODE"
            sender = settings.EMAIL_HOST_USER
            to = email
            title="OTP FOR EMAIL VERIFCATION"
            message="One Time Password For Your Account Regitration"
            ctx = {
                'title':title,
                'otp':otp,
                'content': message,
            }
            message = get_template('email_template/email_otp.html').render(ctx)
            msg = EmailMessage(
                subject,
                message,
                sender,
                [to],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            request.session['otp_from_server']=otp
            request.session['email'] = email
            request.session['password'] = password
            request.session['phone'] = phone
            msg="We have sended you a one time password on your email !!"
            messages.success(request, msg)
            return redirect(verify_otp)
    else:
        return render(request,"user/registration_form.html")

#function for Otp Varification
def verify_otp(request):
    if request.method == "POST":
        email = request.session['email']
        password = request.session['password']
        phone = request.session['phone']
        otp_by_user=str(request.POST['otp_from_user'])
        otp_by_server=str(request.session['otp_from_server'])
        if otp_by_user!=otp_by_server:
            msg="The otp you have enter is incorect !!"
            messages.error(request,msg)
            return redirect(verify_otp)
        else:
            my_user=user(email=email,password=password,phone=phone)
            my_user.save()
            cont="Congratulation You Have Successfully registered"
            send_mail(
                "Registration Successfull",
                cont,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            msg="Your Account is created Now You Can Login"
            request.session.flush()
            messages.success(request,msg)
            return redirect(login)
    else:
        return render(request,'user/verify-otp.html')

def resend_reg_otp(request):
   otp = random.randint(1000, 9999)
   subject = settings.site_name+" OTP For Email Verifcation"
   sender = settings.EMAIL_HOST_USER
   to = request.session['email']
   title = "Email Varification"
   message = "One Time Password For Your Account Regitration"
   ctx = {
                'title': title,
                'otp': otp,
                'content': message,
            }
   message = get_template('email_template/email_otp.html').render(ctx)
   msg = EmailMessage(
   subject,
   message,
   sender,
   [to],
            )
   msg.content_subtype = "html"  # Main content is now text/html
   msg.send()
   request.session['otp_from_server'] = otp
   msg='OTP Resended To Your Email Check Spam Folder '
   messages.success(request, msg)
   return redirect(verify_otp)


def reset_password(request):
    if request.method=="POST":
        email=request.POST['email']
        if user.objects.filter(email=email).exists():
            otp = random.randint(1000, 9999)
            subject = settings.site_name+"  OTP Verification"
            sender =settings.EMAIL_HOST_USER
            to = email
            title = "Email Varification"
            message = "Use The Below Code To Register Your Account "
            ctx = {
                'title': title,
                'otp': otp,
                'content': message,
            }
            message = get_template('email_template/email_otp.html').render(ctx)
            msg = EmailMessage(
                subject,
                message,
                sender,
                [to],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            request.session['otp_from_server'] = otp
            request.session['email'] = email
            msg="Verification Code Sended To Your Email Check Spam Folder If Not Recived"
            messages.success(request,msg)
            return redirect(varify_reset_password_otp)
        else:
            msg = "The Email You Have Provided Is Not Registred With Us !! If Your New To Here You Need To Create Your Account First "
            messages.success(request, msg)
            return redirect(reset_password)
    else:
        return render(request,"user/reset_password_form.html")

def varify_reset_password_otp(request):
    if request.method == "POST":
        email = request.session['email']
        password = request.POST['password']
        otp_by_user= str(request.POST['otp_from_user'])
        otp_by_server = str(request.session['otp_from_server'])
        if otp_by_user != otp_by_server:
            msg="incorrect Otp"
            messages.success(request, msg)
            return redirect(varify_reset_password_otp)
        else:
            my_user=user.objects.get(email=email)
            my_user.password=password
            my_user.save()
            request.session.flush()
            msg="Password Updated Successfully !! Now You Can Login"
            messages.success(request, msg)
            return redirect(login)
    else:
        return render(request,'user/reset_password_varify_otp.html')

def resend_reset_password_otp(request):
    otp = random.randint(1000, 9999)
    # code To Send Otp To Email
    subject = "OTP For Email Verifcation"
    sender = settings.EMAIL_HOST_USER
    to = request.session['email']
    title = "Account Recovery"
    message = "ONE TIME PASSWORD FOR YOUR ACCOUNT RECOVERY"
    ctx = {
        'title': title,
        'otp': otp,
        'content': message,
    }
    message = get_template('email_template/email_otp.html').render(ctx)
    msg = EmailMessage(
        subject,
        message,
        sender,
        [to],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    request.session['otp_from_server'] = otp
    msg="A New OTP Is Sended To Email Check Your Mail Check Spam Folder Also"
    messages.success(request, msg)
    return redirect(varify_reset_password_otp)




#function logoutuser data
def logout(request):
    #del request.session['user_name']
    #del request.session['user_email']
    request.session.flush()
    msg="logout Successfully"
    messages.success(request,msg)
    return redirect(login)