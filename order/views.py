from ckeditor_uploader.utils import get_random_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string

from home.models import Setting
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product
from user.models import UserProfile



def index(request):
    return HttpResponse ("Order Page")

@login_required(login_url='/login') # Check login
def addtoshopcart(request,id):

    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information

    checkproduct = ShopCart.objects.filter(product_id=id) # Check product in shopcart
    if checkproduct:
        control = 1 # The product is in the cart
    else:
        control = 0 # The product is not in the cart

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
           if control==1: # Update  shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
           else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in shopcart:
        total +=  rs.price * rs.quantity
    #return HttpResponse(str(total))
    context={'shopcart': shopcart,
             'category':category,
             'setting':setting,
             'total': total,
             }
    return render(request,'shopcart_products.html',context)


@login_required(login_url='/login') # Check login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total = rs.product.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #

            # Move  Shopcart items to Order Products items
            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in schopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                detail.price        = rs.product.price
                detail.amount        = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount = rs.quantity
                product.save()
                #************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category': category})
        else:
            messages.warning(request, form.errors)


    form= OrderForm()
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'schopcart': schopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               'setting': setting,
               }
    return render(request, 'Order_Form.html', context)