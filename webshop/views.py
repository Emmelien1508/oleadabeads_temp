from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as django_logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic

from pandas import DataFrame
import json

from .models import *
from .forms import LoginForm, RegisterForm
from .utils import *

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "webshop/login.html"

class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'webshop/register.html'
    success_url = reverse_lazy('login')

def home(request):
    cust = get_customer_session(request)

    bestsellers, best = get_sorted_bestsellers()

    return render(request, "webshop/home.html", {
        "bestsellers": bestsellers,
        "best": best
    })

def logout_view(request):
    django_logout(request)
    return redirect(home)

def allproducts(request, soort):
    products, text, name, empty = get_all_products(soort)

    return render(request, "webshop/allproducts.html", {
        "products": products,
        "empty": empty,
        "text": text,
        "name": name
    })

def product(request, naam):
    cust = get_customer_session(request)  

    item, outofstock, added, incart, images = get_product_info(cust, naam)

    message = ""
    if item.left == 0:
        message = "Dit product is uitverkocht!" 

    return render(request, "webshop/product.html", {
        "product": item,
        "outofstock": outofstock,
        "added": added, 
        "incart": incart,
        "images": images,
        "message": message
    })

def diy(request):
    if request.method == 'POST':
        cust = get_customer_session(request)

        jewelrytype, look, chosencolors, metaltype = save_diy_data(request)

        diy = create_diy_product(jewelrytype, look, chosencolors, metaltype)

        create_diy_cartitem(diy, cust)

        return redirect(cart)

    return render(request, "webshop/diy.html")

def about(request):
    return render(request, "webshop/aboutus.html")

def cart(request):
    cust = get_customer_session(request)

    diyproducts, normalproducts, incart, total = get_all_cartitems(cust)

    return render(request, "webshop/cart.html", {
        "diyproducts": diyproducts,
        "normalproducts": normalproducts,
        "total": total,
        "incart": incart,
        "customer": cust
    })

def addtocart(request, naam):
    
    item = Product.objects.get(name = naam)
    cust = get_customer_session(request)

    if request.method == "POST":
        add_product_to_cart(request, cust, item)

        _, outofstock, added, incart, images = get_product_info(cust, naam)

        message = ""
        if item.left == 0:
            message = "Dit product is uitverkocht!" 

        return render(request, "webshop/product.html", {
            "product": item,
            "outofstock": outofstock,
            "added": added, 
            "incart": incart,
            "images": images,
            "message": message,
            "addedtocart": f"{item.name.capitalize()} is aan je winkelmandje toegevoegd!"
        })

def deletefromcart(request, naam):
    cust = get_customer_session(request)

    try:
        item = Product.objects.get(name = naam)
        cartitem = OrderProduct.objects.get(customer = cust, product = item, ordered=False)
    except:
        item = Diy.objects.get(name = naam)
        cartitem = OrderProduct.objects.get(customer = cust, diyproduct = item, ordered=False)

    cartitem.delete()

    return redirect(cart)

def cont(request):
    if request.user.is_anonymous:
        return render(request, "webshop/continuing.html")
    return redirect(checkout)

def checkout(request):
    cust = get_customer_session(request)
    diyproducts, normalproducts, _, subtotal = get_all_cartitems(cust)

    if request.method == "POST":
        cart, payment_option, shipping_option, comments = save_checkout_data(request, cust)
        
        order = create_order(cust, cart, subtotal, payment_option, shipping_option, comments)

        send_email(order, cust, shipping_option)

        return render(request, "webshop/orderconfirmation.html", {
            "cust": cust,
            "order": order,
            "payment": payment_option
        })
    
    freeshipping = False
    if subtotal > 35:
        freeshipping = True

    return render(request, "webshop/checkout.html", {
        "customer": cust,
        "normalproducts": normalproducts,
        "diyproducts": diyproducts,
        "subtotal": subtotal,
        "freeshipping": freeshipping
    })

def contact(request):
    return render(request, "webshop/contact.html")

def profile(request):
    if request.user.is_staff:
        orders = Order.objects.all()

        return render(request, "webshop/admin.html", {
            "orders": orders
        })

    else:
        cust = get_customer_session(request)
        favorites, favitems = get_favorite_info(cust)
        orders = Order.objects.filter(customer = cust)

        return render(request, "webshop/profile.html", {
            "favorites": favorites,
            "favitems": favitems,
            "orders": orders,
            "info": cust,
            "added": True
        })

def order(request, ordernummer):
    order = Order.objects.get(id=ordernummer)

    return render(request, "webshop/order.html", {
        "order": order
    })

def fav(request, naam):
    item = Product.objects.get(name = naam)
    cust = get_customer_session(request)

    try:
        fav = Favorite.objects.get(customer = cust, favoriteproduct = item)
        fav.favoriteproduct.remove(item)
    except:
        try:
            fav = Favorite.objects.get(customer = cust)
        except:
            fav = Favorite.objects.create(customer = cust)
            fav.save()
        fav.favoriteproduct.add(item)

    return redirect(product, naam)

def deletefromprofile(request, naam):
    item = Product.objects.get(name = naam)
    cust = get_customer_session(request)
    fav = Favorite.objects.get(customer = cust, favoriteproduct = item)
    fav.favoriteproduct.remove(item)

    return redirect(profile)

def info(request):
    return render(request, "webshop/information.html")

def discount(request):
    cust = get_customer_session(request)
    diyproducts, normalproducts, incart, total = get_all_cartitems(cust)

    if request.method == "POST":
        code = request.POST["korting"]
        try:
            discount = Discount.objects.get(code = code)
            if discount.active:
                total_after_discount = process_discount(discount, cust, total)
                message = ""
            else:
                message = "De kortingscode is niet meer geldig"
        except:
            message = "De kortingscode is niet geldig"
            total_after_discount = total

    return render(request, "webshop/cart.html", {
        "diyproducts": diyproducts,
        "normalproducts": normalproducts,
        "total": total_after_discount,
        "incart": incart,
        "customer": cust,
        "message": message
    })

def changeprofile(request):
    cust = get_customer_session(request)
    message = ""

    if request.method == "POST":
        change_profile_info(request, cust)
        message = "Gegevens succesvol gewijzigd"

    return render(request, "webshop/change.html", {
        "customer": cust,
        "message": message
    })

def changestatus(request, ordernummer):
    order = Order.objects.get(id = ordernummer)

    if request.method == "POST":
        status = request.POST['orderstatus']
        if order.status == status:
            return render(request, "webshop/changestatus.html", {
                "order": order,
                "message": "Dat is al de huidige status van deze bestelling!"
            })
        elif "Verzonden" in status:
            send_update_email(order)
        order.status = status
        order.save(update_fields=['status'])

    return render(request, "webshop/changestatus.html", {
        "order": order
    })

def terms_conditions(request):
    return render(request, "webshop/terms_and_conditions.html")

def privacypolicy(request):
    return render(request, "webshop/privacy_policy.html")

def disclaimer(request):
    return render(request, "webshop/disclaimer.html")

def guarantee(request):
    return render(request, "webshop/guarantee.html")

def diyproduct(request, idnr):
    product = Diy.objects.get(name = idnr)

    return render(request, "webshop/diyproduct.html", {
        "product": product
    })

def material(request):
    return render(request, "webshop/material_info.html")