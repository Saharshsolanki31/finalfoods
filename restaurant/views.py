from django.shortcuts import render

# Create your views here.
import random
from datetime import datetime
import random
import string
import time

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
from restaurant.models import restaurant, type_of_restaurant, dish_category, dish_type, food_item, FinalAmount, \
    SaveOrders


# login function
def login(request):
    if 'restaurant_email' in request.session:
        return redirect('restaurant_home')
    else:
        if request.method == "POST":
            restaurant_email = request.POST['restaurant_email']
            restaurant_password = request.POST['restaurant_password']
            if restaurant.objects.filter(restaurant_email=restaurant_email).exists():
                if restaurant.objects.filter(restaurant_email=restaurant_email, restaurant_password=restaurant_password).exists():
                    msg = "Login-In Successfuly!! "
                    my_restaurant = restaurant.objects.get(restaurant_email=restaurant_email)
                    request.session['restaurant_email'] = restaurant_email
                    request.session['restaurant_name'] = my_restaurant.restaurant_name
                    messages.success(request,msg)
                    return redirect('restaurant_home')
                else:
                    msg = "Inccorect Password !"
                    messages.success(request, msg)
                    return redirect(login)
            else:
                msg = "Email is Not Registered !"
                messages.success(request, msg)
                return redirect(register)
        else:
          return render(request, "restaurant/login.html")


def restaurant_home(request):
    if 'restaurant_email' in request.session:
        return render(request,'restaurant/home.html')
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def menu(request):
    if 'restaurant_email' in request.session:
        if request.method == "POST":
            dish_types = dish_type.objects.get(id=request.POST[''])
            dish_cat = request.POST['dish_category']
        else:
            res_id = restaurant.objects.get(restaurant_email = request.session['restaurant_email'])
            dish_types = dish_type.objects.all()
            if 'search' in request.GET:
                dish_cat = dish_category.objects.filter(name__icontains=request.GET['search'],rest_id=res_id)
            else:
                dish_cat = dish_category.objects.filter(rest_id=res_id)
            return render(request,'restaurant/menu.html',{'dish_type':dish_types,'dish_cat':dish_cat})
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)



def add_food_item(request):
    if 'restaurant_email' in request.session:
        if request.method == 'POST':
            res_id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            item_name =request.POST['item_name']
            food_image = request.FILES['food_image']
            item_price = request.POST['item_price']
            item_dish_category = dish_category.objects.get(id=int(request.POST['dish_category_id']))
            dish_type_item = dish_type.objects.get(id=int(request.POST['dish_type_id']))
            if food_item.objects.filter(item_name=item_name,restaurant_id=res_id,item_price=item_price,dish_category=item_dish_category,dish_type=dish_type_item).exists():
                messages.success(request, 'This Food is Already Exists !')
                return redirect(add_food_item)
            else:
                data = food_item(item_name=item_name,restaurant_id=res_id,item_image=food_image,item_price=item_price,dish_category=item_dish_category,dish_type=dish_type_item)
                data.save()
                messages.success(request,'Food item added succssfully')
                return redirect(add_food_item)
        else:
            res_id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            dish_types = dish_type.objects.all()
            dish_categorys = dish_category.objects.filter(rest_id = res_id)
            if 'search' in request.GET:
                items_data = food_item.objects.filter(item_name__icontains=request.GET['search'],restaurant_id = res_id)
            else:
                items_data = food_item.objects.filter(restaurant_id=res_id)
            return render(request,'restaurant/add_food_item.html',{'dish_type':dish_types,'dish_category':dish_categorys,'food_data':items_data})
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)



def add_dish_category(request):
    if 'restaurant_email' in request.session:
        if request.method == 'POST':

            res_id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            dish_category_name =request.POST['dish_category']
            x=dish_category_name.split(',')
            print(x[0].split('='))
            if dish_category.objects.filter(name=dish_category_name,rest_id=res_id).exists():
                messages.success(request, 'Menu name Already Exists !')
                return redirect(menu)
            else:
                data = dish_category(name=dish_category_name,rest_id=res_id)
                data.save()
                messages.success(request,'Added Successfully')
                return redirect(menu)
        else:

            return redirect(menu)
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def edit_menu_item(request,id):
    if 'restaurant_email' in request.session:
            res_id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            dish_categorys = dish_category.objects.get(id=id)
            return render(request,'restaurant/edit_menu_item.html',{'data':dish_categorys})
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def update_menu_item(request):
    if 'restaurant_email' in request.session:
        if request.method == "POST":
            # res_id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            id =request.POST['id']
            dish = request.POST['dish_category']
            data =dish_category.objects.get(id=id)
            data.name=dish
            data.save()
            messages.success(request,'Update sucessfully !')
            return redirect(menu)
        else:
            return redirect(menu)
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def delete_menu_item(request,id):
    if 'restaurant_email' in request.session:
        dish_categorys = dish_category.objects.get(id=id)
        dish_categorys.delete()
        messages.success(request,'Deleted Successfully')
        return redirect(menu)
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)



def edit_food_item(request,id):
    if 'restaurant_email' in request.session:
            res_id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            food_data = food_item.objects.get(id=id)
            dish_types = dish_type.objects.all()
            dish_cat = dish_category.objects.filter(rest_id=res_id)
            return render(request,'restaurant/edit_food_item.html',{'data':food_data,'dish_type':dish_types,'dish_category':dish_cat})
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def update_food_item(request):
    if 'restaurant_email' in request.session:
        if request.method == "POST":
            id=request.POST['id']
            item_name = request.POST['item_name']
            item_price = request.POST['item_price']
            item_dish_type = dish_type.objects.get(id=request.POST['dish_type'])
            item_dish_category = dish_category.objects.get(id = request.POST['dish_category'])
            res_id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            food_data = food_item.objects.get(id=id)
            food_data.item_name = item_name
            food_data.item_price = item_price
            food_data.dish_type = item_dish_type
            food_data.dish_category=item_dish_category
            if 'item_image' in request.FILES:
                food_data.item_image=request.FILES['item_image']
            food_data.save()
            messages.success(request,'Updated Successfully')
            return redirect(add_food_item)
        else:
            return redirect(add_food_item)
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def delete_food_item(request,id):
    if 'restaurant_email' in request.session:
        data = food_item.objects.get(id=id)
        data.delete()
        messages.success(request,'Deleted Successfully')
        return redirect(add_food_item)
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)




def table(request):
    if 'restaurant_email' in request.session:
        if 'search' in request.POST:
            search = request.POST['search']
            id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            orderid = SaveOrders.objects.filter(restaurant_id=id,orderid__icontains=search).values('orderid').distinct()
            all_orders = SaveOrders.objects.all()
            finalprice = FinalAmount.objects.filter(restaurant_id=id)
        else:
            id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            orderid = SaveOrders.objects.filter(restaurant_id=id).values('orderid').distinct()
            all_orders = SaveOrders.objects.all()
            finalprice = FinalAmount.objects.filter(restaurant_id=id)

        return render(request, "restaurant/table.html",
                      {"all_orders": all_orders, "orderid": orderid, "finalprice": finalprice})
    else:
        messages.error(request, 'session expired ! Logsin Again')
        return redirect(login)

def make_new_order(request):
    if 'restaurant_email' in request.session:
        if 'search' in request.POST:
            search = request.POST['search']
            dish = food_item.objects.filter(item_name__icontains=search)
        else:
            dish = food_item.objects.all()
        epoch = time.time()
        user_id = random.randint(1000,9999)  # this could be incremental or even a uuid
        orderid = "%s_%d" % (user_id, epoch)
        return render(request, 'restaurant/make_new_order.html', {"dish": dish,"orderid":orderid})
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)

def on_order(request,id):
    if 'restaurant_email' in request.session:
        if 'search' in request.POST:
            search = request.POST['search']
            dish = food_item.objects.filter(item_name__icontains=search)
        else:
            dish = food_item.objects.all()
        orderid = id
        see_orders = SaveOrders.objects.filter(orderid=orderid)
        return render(request, 'restaurant/make_new_order.html', {"dish": dish,"orderid":orderid,"see_orders":see_orders})
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)


def update_item_quantity(request,id):
    if 'restaurant_email' in request.session:
        item = SaveOrders.objects.get(id=id)
        item.quantity =request.POST['quantity']
        item.item_price=request.POST['item_price']
        item.total=float(item.quantity)*float(item.item_price)
        orderid=item.orderid
        item.save()
        messages.success(request,"Quantity update")
        return redirect(on_order,id=orderid)
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)

def cancel_item(request,id):
    if 'restaurant_email' in request.session:
        item = SaveOrders.objects.get(id=id)
        orderid=item.orderid
        item.delete()
        messages.success(request,"Item Deleted")
        return redirect(on_order,id=orderid)
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)

def confirm_order(request):
    if 'restaurant_email' in request.session:
        orderid=request.POST['orderid']
        items = SaveOrders.objects.filter(orderid=orderid)
        final=0
        for item in items:
            total=item.total
            final=float(final)+float(total)
        print(final)
        final_price=final
        data=FinalAmount(orderid=orderid,final_price=final_price,restaurant_id=restaurant.objects.get(restaurant_email=request.session['restaurant_email']))
        data.save()
        messages.success(request,"order Confirm")
        return redirect(pending_order)
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)


def save_order(request):
    if 'restaurant_email' in request.session:
        dish = food_item.objects.all()
        item_name = request.GET['item_name']
        item_price = request.GET['item_price']
        dish_type = request.GET['dish_type']
        orderid=request.GET['orderid']
        quantity=request.GET['quantity']
        total=float(item_price)*float(quantity)
        order_save=SaveOrders(item_name=item_name,item_price=item_price,restaurant_id=restaurant.objects.get(restaurant_email=request.session['restaurant_email']),dish_type=dish_type,orderid=orderid,quantity=quantity,total=total)
        order_save.save()
        see_orders=SaveOrders.objects.filter(orderid=orderid)
        messages.success(request,"order saved")
        return redirect('on_order',id=orderid)
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)


def complete_order(request):
    if 'restaurant_email' in request.session:
        if 'search' in request.POST:
            search=request.POST['search']
            id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            orderid = SaveOrders.objects.filter(status='complete', restaurant_id=id,orderid__icontains=search).values('orderid').distinct()
            complete_orders = SaveOrders.objects.filter(status='complete')
            finalprice = FinalAmount.objects.filter(restaurant_id=id)
        else:
            id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            orderid = SaveOrders.objects.filter(status='complete', restaurant_id=id).values('orderid').distinct()
            complete_orders = SaveOrders.objects.filter(status='complete')
            finalprice = FinalAmount.objects.filter(restaurant_id=id)

        return render(request, "restaurant/complete_order.html",
                      {"complete_orders": complete_orders, "orderid": orderid, "finalprice": finalprice})
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)

def complete_order_status(request,id):
    if 'restaurant_email' in request.session:
        id = SaveOrders.objects.get(id=id)
        id.status = 'complete'
        id.save()
        messages.success(request,"order complete")
        return redirect(pending_order)
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)

def cancel_order_status(request,id):
    if 'restaurant_email' in request.session:
        id = SaveOrders.objects.get(id=id)
        amount=id.total
        orderid=id.orderid
        finalamount=FinalAmount.objects.get(orderid=orderid,restaurant_id=restaurant.objects.get(restaurant_email=request.session['restaurant_email']))
        famount=finalamount.final_price
        remaning=float(famount)-float(amount)
        finalamount.final_price=remaning
        finalamount.save()
        id.delete()

        messages.success(request,"order cancel")
        return redirect(pending_order)
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)

def pending_order(request):
    if 'restaurant_email' in request.session:
        if 'search' in request.POST:
            search=request.POST['search']
            id = restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            orderid = SaveOrders.objects.filter(status='pending', restaurant_id=id,orderid__icontains=search).values('orderid').distinct()
            pending_orders = SaveOrders.objects.filter(status='pending')
            finalprice = FinalAmount.objects.filter(restaurant_id=id)
        else:
            id=restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            orderid=SaveOrders.objects.filter(status='pending',restaurant_id=id).values('orderid').distinct()
            pending_orders=SaveOrders.objects.filter(status='pending')
            finalprice=FinalAmount.objects.filter(restaurant_id=id)

        return render(request,"restaurant/pending_order.html",{"pending_orders":pending_orders,"orderid":orderid,"finalprice":finalprice})
    else:
        messages.error(request, 'session expired ! Login Again')
        return redirect(login)

def orders(request):
    if 'restaurant_email' in request.session:
        return render(request,'restaurant/orders.html')
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def register(request):
    if request.method=="POST":
        restaurant_type = request.POST['restaurant_type']
        restaurant_name = request.POST['restaurant_name']
        restaurant_email = request.POST['restaurant_email']
        restaurant_mobile_number = request.POST['restaurant_mobile_number']
        restaurant_password = request.POST['restaurant_password']
        restaurant_address = request.POST['restaurant_address']
        restaurant_city = request.POST['restaurant_city']
        restaurant_state = request.POST['restaurant_state']
        restaurant_pincode = request.POST['restaurant_pincode']
        if restaurant.objects.filter(restaurant_email=restaurant_email).exists():
            msg="You have Already Registered !"
            messages.error(request,msg)
            return redirect(register)
        elif restaurant.objects.filter(restaurant_mobile_number=restaurant_mobile_number).exists():
            msg = "Mobile Number is linked With Another Account !"
            messages.error(request, msg)
            return redirect(register)
        else:
            otp=random.randint(1000,9999)
            subject = "ONE TIME PASSWORD VERIFCTAION CODE"
            sender = settings.EMAIL_HOST_USER
            to = restaurant_email
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
            request.session['restaurant_name'] = restaurant_name
            request.session['restaurant_email'] = restaurant_email
            request.session['restaurant_mobile_number'] = restaurant_mobile_number
            request.session['restaurant_password'] = restaurant_password
            request.session['restaurant_address'] = restaurant_address
            request.session['restaurant_city'] = restaurant_city
            request.session['restaurant_state'] = restaurant_state
            request.session['restaurant_pincode'] = restaurant_pincode
            request.session['restaurant_type'] = restaurant_type
            msg="We have sended you a one time password on your email !!"
            messages.success(request, msg)
            return redirect(verify_otp)
    else:
        restaurant_type = type_of_restaurant.objects.all()
        return render(request,"restaurant/registration_form.html",{'restaurant_type':restaurant_type})

#function for Otp Varification
def verify_otp(request):
    if request.method == "POST":
        restaurant_name = request.session['restaurant_name']
        restaurant_email =   request.session['restaurant_email']
        restaurant_mobile_number = request.session['restaurant_mobile_number']
        restaurant_password   =  request.session['restaurant_password']
        restaurant_address    =   request.session['restaurant_address']
        restaurant_city       =  request.session['restaurant_city']
        restaurant_state      =  request.session['restaurant_state']
        restaurant_pincode    =  request.session['restaurant_pincode']
        restaurant_type =request.session['restaurant_type']
        otp_by_restaurant=str(request.POST['otp_from_restaurant'])
        otp_by_server=str(request.session['otp_from_server'])
        if otp_by_restaurant!=otp_by_server:
            msg="The otp you have enter is incorect !!"
            messages.error(request,msg)
            return redirect(verify_otp)
        else:
            rest_type = type_of_restaurant.objects.get(id=int(restaurant_type))
            my_restaurant=restaurant(restaurant_name=restaurant_name,restaurant_type=rest_type,restaurant_email=restaurant_email,restaurant_password = restaurant_password,restaurant_mobile_number=restaurant_mobile_number,restaurant_address=restaurant_address,restaurant_city=restaurant_city,restaurant_state=restaurant_state,restaurant_pincode=restaurant_pincode)
            my_restaurant.save()
            cont="Congratulation You Have Successfully registered"
            send_mail(
                "Registration Successfull",
                cont,
                settings.EMAIL_HOST_USER,
                [restaurant_email],
                fail_silently=False,
            )
            msg="Your Account is created Now You Can Login"
            request.session.flush()
            messages.success(request,msg)
            return redirect(login)
    else:
        return render(request,'restaurant/verify-otp.html')

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
   return JsonResponse({'status':0,'msg':msg})


def reset_password(request):
    if request.method=="POST":
        email=request.POST['email']
        if restaurant.objects.filter(restaurant_email=email).exists():
            otp = random.randint(1000, 9999)
            subject = settings.site_name+"  OTP Verification"
            sender =  settings.EMAIL_HOST_USER
            to = email
            title = "Account Recovery"
            message = "Use The Below Code To Recovery Your Account "
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
            #now We Need To Genrate 4 Digit Random Number And Send It To Mail
            msg = "The Email You Have Provided Is Not Registred With Us !! If Your New To Here You Need To Create Your Account First "
            messages.success(request, msg)
            return redirect(reset_password)
    else:
        return render(request,"restaurant/reset_password_form.html")

def varify_reset_password_otp(request):
    if request.method == "POST":
        email = request.session['email']
        password = request.POST['password']
        otp_by_restaurant= str(request.POST['otp_from_restaurant'])
        otp_by_server = str(request.session['otp_from_server'])
        if otp_by_restaurant != otp_by_server:
            msg="Inccorect OTP !!"
            messages.success(request, msg)
            return redirect(varify_reset_password_otp)
        else:
            my_restaurant=restaurant.objects.get(email=email)
            my_restaurant.restaurant_password=password
            my_restaurant.save()
            request.session.flush()
            msg="Password Updated Successfully Now You Can Login"
            messages.success(request, msg)
            return redirect(login)
    else:
        return render(request,'restaurant/reset_password_varify_otp.html')

def resend_reset_password_otp(request):
    otp = random.randint(1000, 9999)
    # code To Send Otp To Email
    subject = "Account Recovery"
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
    msgs="A New OTP Is Sended To Email Check Your Mail Check Spam Folder Also"
    messages.success(request, msgs)
    return redirect(varify_reset_password_otp)




#function logoutrestaurant data
def logout(request):
    request.session.flush()
    msg="logout Successfully"
    messages.success(request,msg)
    return redirect(login)