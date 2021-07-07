from django.shortcuts import render

# Create your views here.
import random
from datetime import datetime
import random
import time
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
from restaurant.models import restaurant, dish_category, food_item
from user.models import user, cart, address, user_order_id, user_order_item, order_history


def home(request):
    if 'user_email' in request.session:
        return render(request,'user/home.html')
    else:
        return redirect(login)


def gen_order_id(size):
    chars = string.ascii_lowercase + string.digits
    x=""
    for p in range(size):
        x=x+random.choice(string.ascii_uppercase + string.digits)
    rn = random.randint(10000,99999)
    return "OR_"+x+str(rn)



def do_checkout_pickup(request):
    if 'user_email' in request.session:
        if request.method =="POST":
            delivery_type = request.POST['delivery_type']
            if delivery_type =="unselected":
                messages.success(request,'Selected Delivery Type')
                return redirect(user_cart)
            else:
                user_email = request.session['user_email']
                cart_data = cart.objects.filter(user_email=user_email)
                total = 0
                lst = []
                for c in cart_data:
                    lst.append(c.food_id.id)
                    total = total + float(c.food_total_price)
                food_data = food_item.objects.filter(id__in=lst)
                address_data = address.objects.filter(user_id=user.objects.get(email=user_email))
                try:
                    if address_data[0]:
                        return render(request, 'user/checkout.html',
                                  {'cart_data': cart_data, 'food_data': food_data, 'total': total,'delivery_type':delivery_type,'address':address_data})
                except:
                    messages.success(request,"Please add atleast one addess !!")
                    return redirect(add_address)
    else:
        messages.error(request,"login first !!")
        return redirect(login)




def do_checkout_delivery(request):
    if 'user_email' in request.session:
        if request.method =="POST":
            if request.POST['address'] == "none":
                messages.error(request, "Select Delivery Address !!")
                return redirect(user_cart)
            user_email = request.session['user_email']
            cart_data = cart.objects.filter(user_email=user_email)
            user_id = user.objects.get(email=request.session['user_email'])
            delivery_type = "delivery"
            payment_method = request.POST['payment_method']
            address_id = address.objects.get(id=request.POST['address'])
            order_id = gen_order_id(10)
            make_order = user_order_id(order_id=order_id,order_type=delivery_type,user_id=user_id,address_id=address_id,payment_type=payment_method)
            make_order.save()
            order_id_data =user_order_id.objects.get(order_id=order_id)
            for c in cart_data:
                data = user_order_item(user_email=user_id,user_order_id=order_id_data,food_quantity=c.food_quantity,food_total_price=c.food_total_price,food_id=c.food_id)
                data.save()
            total = 0
            lst = []
            for c in cart_data:
                lst.append(c.food_id.id)
                total = total + float(c.food_total_price)

            make_order_history = order_history(my_user_id=user_id,my_order_id=order_id_data,amount=total)
            make_order_history.save()
            for c in cart_data:
                my_data = cart.objects.get(id=c.id)
                my_data.delete()
            messages.success(request,'Order placed suucssfully')
            return redirect(user_cart)
        else:
            messages.success(request, "We Got Some error try again !!")
            return redirect(user_cart)

    else:
        messages.error(request,"login first !!")
        return redirect(login)




def checkout(request):
    if 'user_email' in request.session:
        if request.method =="POST":
            delivery_type = request.POST['delivery_type']
            if delivery_type =="unselected":
                messages.success(request,'Selected Delivery Type')
                return redirect(user_cart)
            else:
                user_email = request.session['user_email']
                cart_data = cart.objects.filter(user_email=user_email)
                total = 0
                lst = []
                for c in cart_data:
                    lst.append(c.food_id.id)
                    total = total + float(c.food_total_price)
                food_data = food_item.objects.filter(id__in=lst)
                address_data = address.objects.filter(user_id=user.objects.get(email=user_email))
                try:
                    if address_data[0]:
                        return render(request, 'user/checkout.html',
                                  {'cart_data': cart_data, 'food_data': food_data, 'total': total,'delivery_type':delivery_type,'address':address_data})
                except:
                    messages.success(request,"Please add atleast one addess !!")
                    return redirect(add_address)
    else:
        messages.error(request,"login first !!")
        return redirect(login)




def add_address(request):
    if 'user_email' in request.session:
        user_email = user.objects.get(email=request.session['user_email'])
        if request.method == "POST":
            name = request.POST['user_name']
            user_address = request.POST['address']
            city = request.POST['city']
            if 'landmark' in request.POST:
                landmark= request.POST['landmark']
            else:
                landmark = ""
            pincode = request.POST['pincode']
            state = request.POST['state']
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            mobile_number = request.POST['mobile_number']
            alternate_mobile_number = request.POST['alternate_mobile_number']
            data  = address(user_id = user_email,name = name ,latitude=latitude,longitude=longitude, address= user_address,city=city,landmark=landmark,pincode=pincode,state=state,mobile_number=mobile_number,alternate_mobile_number=alternate_mobile_number)
            data.save()
            messages.success(request,'New Address Is Added !!')
            return redirect(add_address)
        else:
            data = address.objects.filter(user_id = user_email)
            return render(request,'user/address.html', {'address_data':data})
    else:
        messages.error(request,'Login first !!')
        return redirect(login)



def delete_user_address(request,id):
    if 'user_email' in request.session:
        data = address.objects.get(id=id)
        data.delete()
        messages.success(request, 'Address Deleted !!')
        return redirect(add_address)
    else:
        return redirect(login)




def edit_user_address(request,id):
    if 'user_email' in request.session:
        if request.method == "POST":
            data = address.objects.get(id=id)
            data.name = request.POST['user_name']
            data.address = request.POST['address']
            data.city = request.POST['city']
            data.landmark = request.POST['landmark']
            data.pincode = request.POST['pincode']
            data.state = request.POST['state']
            data.latitude = request.POST['latitude']
            data.longitude = request.POST['longitude']
            data.mobile_number = request.POST['mobile_number']
            data.alternate_mobile_number = request.POST['alternate_mobile_number']
            data.save()
            messages.success(request, 'Address Updated Succssfully !!')
            return redirect(add_address)
        else:
            data = address.objects.get(id=id)
            return render(request,'user/edit_user_address.html',{'data':data,'id':id})
    else:
        return redirect(login)







def update_item_quantity(request,type,id):
    if 'user_email' in request.session:
        if type == "add":
            cart_data = cart.objects.get(id=id)
            food_data = food_item.objects.get(id=cart_data.food_id.id)
            cart_data.food_quantity = int(cart_data.food_quantity) + 1
            cart_data.food_total_price = float(cart_data.food_total_price) + float(food_data.item_price)
            cart_data.save()
            messages.success(request, 'Quantity Updated !!')
            return redirect(user_cart)
        else:
            cart_data = cart.objects.get(id=id)
            food_data = food_item.objects.get(id=cart_data.food_id.id)
            if int(cart_data.food_quantity) <= 1:
                data = cart.objects.get(id=id)
                data.delete()
                messages.success(request, 'item quantity is already 1 so we have removed the product from cart !!')
                return redirect(user_cart)
            else:
                cart_data.food_quantity = int(cart_data.food_quantity) - 1
                cart_data.food_total_price = float(cart_data.food_total_price) - float(food_data.item_price)
                cart_data.save()
                messages.success(request, 'Quantity Updated !!')
                return redirect(user_cart)
                messages.success(request, 'Quantity Updated !!!')
                return redirect(user_cart)
    else:
        messages.warning(request, 'You need to login first !!')
        return redirect(login)



def remove_item_from_cart(request,id):
    if 'user_email' in request.session:
        data = cart.objects.get(id=id)
        data.delete()
        messages.success(request, ' item removed form cart !!')
        return redirect(user_cart)
    else:
        messages.warning(request, 'You need to login first !!')
        return redirect(login)


def user_cart(request):
    if 'user_email' in request.session:
        user_email = request.session['user_email']
        cart_data = cart.objects.filter(user_email = user_email)
        total = 0
        lst = []
        for c in cart_data:
            lst.append(c.food_id.id)
            total = total + float(c.food_total_price)
        food_data  = food_item.objects.filter(id__in=lst)
        return render(request,'user/cart.html',{'cart_data':cart_data,'food_data':food_data,'total':total})
    else:
        messages.warning(request,'You need to login first !!')
        return redirect(login)


def add_to_cart(request):
    if 'user_email' in request.session:
        food_id = request.GET['food_id']
        if cart.objects.filter(food_id=food_id,user_email = request.session['user_email']).exists():
            food_data = food_item.objects.get(id=food_id)
            rest_id = food_data.restaurant_id_id
            cart_data = cart.objects.get(user_email=request.session['user_email'],food_id= food_id)
            cart_data.food_quantity = int(cart_data.food_quantity)+1
            cart_data.food_total_price = float(cart_data.food_total_price) + float(food_data.item_price)
            cart_data.save()
            msg = "This Item Is Already Availabe In Your Cart We Have Updated Its Quantity"
        else:
            food_data = food_item.objects.get(id=food_id)
            add_cart = cart(user_email=request.session['user_email'],food_quantity=1,food_total_price = food_data.item_price,food_id=food_data)
            add_cart.save()
            rest_id = food_data.restaurant_id_id
            msg="Item Added to your cart goto cart"
        messages.success(request,msg)
        return redirect('order_from_restaurant',id=rest_id)
    else:
        msg = "You Need To Login !!"
        messages.success(request, msg)
        return redirect(login)



def order_from_restaurant(request,id):
    rest_id = restaurant.objects.get(id=id)
    dish = dish_category.objects.filter(rest_id = rest_id)
    food_data = food_item.objects.filter(restaurant_id=rest_id)
    rest_data = restaurant.objects.get(id=id)
    return render(request,"user/restaurant_detail.html",{'restaurant':rest_data,'dish_category':dish,'food_data':food_data})

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