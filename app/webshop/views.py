from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import logout as django_logout
from .models import *
from datetime import *
from django.contrib.auth import views as auth_views
from django.views import generic
from .forms import LoginForm, RegisterForm
from django.urls import reverse_lazy
import datetime
import operator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .utils import get_customer_session

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "webshop/login.html"

class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'webshop/register.html'
    success_url = reverse_lazy('login')

def home(request):
    cust = get_customer_session(request)

    sold_items = OrderProduct.objects.filter(ordered=True).order_by("product")
    products = {}

    for item in sold_items:
        try:
            products[item.product.name] += item.quantity
        except:
            products[item.product.name] = item.quantity

    sorted_bestsellers = dict(sorted(products.items(), key=operator.itemgetter(1),reverse=True))
    bestsellers = [product for title in sorted_bestsellers.keys() for product in Product.objects.all() if product.name == title]

    if len(bestsellers) > 4:
        bestsellers = bestsellers[0:4]
    
    best = True
    if not bestsellers:
        best = False

    return render(request, "webshop/home.html", {
        "bestsellers": bestsellers,
        "best": best
    })

def logout_view(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
        del s
    except:
        pass
    
    django_logout(request)
    return redirect(home)

def allproducts(request, soort):
    if soort == 'nieuw':
        orderedproducts = list(Product.objects.all().order_by("-date_added"))
        products = [product for product in orderedproducts]
        text = "Hieronder staan alle producten die nieuw zijn toegevoegd!"
        name = "Nieuw"

        if len(products) > 20:
            products = products[0:20]

    if soort == "bestsellers":
        sold_items = OrderProduct.objects.filter(ordered=True).order_by("product")
        bestsellers = {}
        for item in sold_items:
            try:
                bestsellers[item.product.name] += item.quantity
            except:
                bestsellers[item.product.name] = item.quantity    
        sorted_bestsellers = dict(sorted(bestsellers.items(), key=operator.itemgetter(1),reverse=True))
        products = [product for title in sorted_bestsellers.keys() for product in Product.objects.all() if product.name == title]
        text = "Al onze bestsellers zijn op deze pagina te vinden!"
        name = "Bestsellers"

        if len(products) > 20:
            products = products[0:20]
    
    if soort == "limitededitions":
        products = [product for product in Product.objects.all() if product.limited_edition == True]
        text = "Je vindt hieronder al onze limited edition producten. Op = op!"
        name = "Limited Editions"

    if soort == "kettingen":
        products = [product for product in Product.objects.all() if product.jewelry_type == "Ketting"]
        text = "Op deze pagina vindt je onze handgemaakte kettingen. Deze zijn super leuk om te combineren met onze hangers, go check it out!"
        name = "Kettingen"

    if soort == "armbanden":
        products = [product for product in Product.objects.all() if product.jewelry_type == "Armband"]
        text = "Deze zelfgemaakte armbandjes zijn perfect om te combineren!"
        name = "Armbanden"

    if soort == "oorbellen":
        products = [product for product in Product.objects.all() if product.jewelry_type == "Oorbel"]
        text = "De oorbellen op deze pagina staan heel leuk samen, dus lekker mixen & matchen! De prijzen zijn per stuk."
        name = "Oorbellen"

    if soort == 'hangers':
        products = [product for product in Product.objects.all() if product.jewelry_type == 'Hanger']
        text = "De hangers op deze pagina zijn bedoeld om te combineren met onze leuke kettingen!"
        name = "Hangers"

    empty = False
    if not products:
        empty = True

    return render(request, "webshop/allproducts.html", {
        "products": products,
        "empty": empty,
        "text": text,
        "name": name
    })

def product(request, naam):
    item = Product.objects.get(name=naam)
    outofstock = True
    if item.in_stock:
        outofstock = False

    images = item.image.all()

    cust = get_customer_session(request)

    if item.left == 0:
        message = "Dit product is uitverkocht!"
    else:
        message = ""

    try:
        # als dit lukt dan bestaat deze item in de cart vd user
        cartitem = OrderProduct.objects.get(customer = cust, product = item)
        incart = True
    except:
        incart = False

    try:
        # als dit lukt dan bestaat deze item in de fav list vd user
        fav = Favorite.objects.get(customer = cust, favoriteproduct = item)
        added = True
    except:
        added = False

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

        # gegevens opvragen van form
        diyjewelrytype = request.POST['jewelrytype']
        diylook = request.POST['look']
        diycolor = request.POST.getlist('color[]')
        chosencolors = [Color.objects.get(color = col) for col in diycolor]
        diymetaltype = request.POST['metaltype']

        # product aanmaken en prijsverschil berekenen
        diy = Diy()
        diy.price = 5
        if diyjewelrytype == "Ketting":
            diy.price += 2
        if diylook == "Schakelketting":
            diy.price += 1.50
        if "Edelsteen" in diycolor:
            diy.price += 1.50
        if "Parel" in diycolor:
            diy.price += 1
        if diymetaltype == "Goud":
            diy.price += 0.5

        diy.jewelry_type = diyjewelrytype
        diy.look = diylook
        diy.metal_type = diymetaltype
        diy.save()
        diy.name = str(diy.id)
        diy.color.set(chosencolors)
        
        cartproduct = OrderProduct()
        cartproduct.diyproduct = diy
        cartproduct.customer = cust
        cartproduct.ordered = False
        cartproduct.quantity = 1
        cartproduct.save()

        # return redirect(home)
        return redirect(cart)

    return render(request, "webshop/diy.html", {
        "range": range(16)
    })

def about(request):
    return render(request, "webshop/aboutus.html")

def cart(request):
    cust = get_customer_session(request)

    cartitems = [item for item in OrderProduct.objects.filter(customer = cust, ordered = False)]

    incart = True
    if not cartitems:
        incart = False
    
    total = 0
    for item in cartitems:
        total += item.quantity * item.product.price

    # return redirect(home)
    return render(request, "webshop/cart.html", {
        "incart": incart,
        "cartitems": cartitems,
        "total": total,
        "customer": cust
    })

def addtocart(request, naam):
    item = Product.objects.get(name = naam)
    
    cust = get_customer_session(request)

    if request.method == "POST":
        amount = int(request.POST["hoeveelheid"])
        # kijken of dit product al in de winkelwagen zit
        if OrderProduct.objects.filter(customer = cust, product = item, ordered = False).exists():
            # als dit kan zit dat product er al in
            cartproduct = OrderProduct.objects.get(customer = cust, product = item, ordered = False)
            cartproduct.quantity += amount
            cartproduct.save()
        else:
            cartproduct = OrderProduct()
            cartproduct.product = item
            cartproduct.customer = cust
            cartproduct.ordered = False
            cartproduct.quantity = amount
            cartproduct.save()

    return redirect(product, naam)

def deletefromcart(request, naam):
    item = Product.objects.get(name = naam)

    cust = get_customer_session(request)

    cartitem = OrderProduct.objects.get(customer = cust, product = item, ordered=False)
    cartitem.delete()

    if item.name == "DIY":
        item.delete()

    return redirect(cart)

def cont(request):
    if request.user.is_anonymous:
        return render(request, "webshop/continuing.html")
    return redirect(checkout)

def checkout(request):
    if request.method == "POST":
        straat = request.POST['streetname']
        huisnr = request.POST['housenr']
        postcode = request.POST['postalcode']
        stad = request.POST['city']
        betaalwijze = request.POST['payment_option']
        voornaam = request.POST['voornaam']
        achternaam = request.POST['achternaam']
        email = request.POST['email']

        cust = get_customer_session(request)

        if request.user.is_anonymous:
            cartitems = OrderProduct.objects.filter(customer = cust, ordered = False)
            cust.firstname = voornaam
            cust.lastname = achternaam
            cust.email = email
        else:
            cartitems = OrderProduct.objects.filter(customer = cust, ordered = False)
            voornaam = cust.firstname
            achternaam = cust.lastname
            email = cust.email

        cust.streetname = straat
        cust.housenr = huisnr
        cust.postalcode = postcode
        cust.city = stad

        try:
            cust.save(update_fields=['email', 'firstname', 'lastname', 'streetname', 'housenr', 'postalcode', 'city'])
        except:
            pass
        
        total = 0
        for item in cartitems:
            total += item.quantity * item.product.price
            item.ordered = True
            item.save(update_fields=['ordered'])

        order = Order()
        order.customer = cust
        order.date_ordered = datetime.datetime.now()
        order.status = "Ontvangen"
        order.total = total
        order.save()
        order.orderproduct.set(cartitems)

        context = {
            "order": order,
            "customer": cust
        }

        subject = f"Dankjewel voor je bestelling {cust.firstname}!"
        msg_plain = render_to_string("webshop/email.txt", context)
        msg_html = render_to_string("webshop/email.html", context)
        from_email = settings.EMAIL_HOST_USER
        to_list = [f"{cust.email}"]

        send_mail(
            subject,
            msg_plain,
            from_email,
            to_list,
            html_message=msg_html,
            fail_silently=True,
        )

        return render(request, "webshop/orderconfirmation.html", {
            "customer": cust,
            "cart": order,
            "total": total
        })

    cust = get_customer_session(request)

    cartitems = OrderProduct.objects.filter(customer = cust, ordered=False)
    total = 0
    for item in cartitems:
        total += item.quantity * item.product.price

    return render(request, "webshop/checkout.html", {
        "customer": cust,
        "cart": cartitems,
        "total": total
    })

def contact(request):
    return render(request, "webshop/contact.html")

def photos(request):
    return render(request, "webshop/photos.html")

def profile(request):
    cust = Customer.objects.get(email = request.user.email)
    favorites = Favorite.objects.filter(customer = cust)
    faves = [product for fav in favorites for product in fav.favoriteproduct.all()]
    print(faves)
    orders = Order.objects.filter(customer = cust)

    favitems = False
    if faves:
        favitems = True

    return render(request, "webshop/profile.html", {
        "favorites": faves,
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

def addtofav(request, naam):
    item = Product.objects.get(name = naam)
    cust = Customer.objects.get(email = request.user.email)

    # kijken of er al een favorite verlanglijst van de user bestaat
    try: 
        Favorite.objects.get(customer = cust)
        fav = Favorite.objects.get(customer = cust)
        fav.favoriteproduct.add(item)
    except:
        fav = Favorite()
        fav.customer = cust
        fav.save()
        fav.favoriteproduct.add(item)
    
    return redirect(product, naam)

def deletefromfav(request, naam):
    cust = Customer.objects.get(email = request.user.email)

    item = Product.objects.get(name = naam)
    fav = Favorite.objects.get(customer = cust, favoriteproduct = item)
    fav.delete()
    return redirect(product, naam)

def deletefromprofile(request, naam):
    cust = Customer.objects.get(email = request.user.email)

    item = Product.objects.get(name = naam)
    fav = Favorite.objects.get(customer = cust, favoriteproduct = item)
    print(fav)
    print(Favorite.objects.all())
    fav.delete()
    print(Favorite.objects.all())
    return redirect(profile)

def fav(request):
    cust = Customer.objects.get(email = request.user.email)

    favorites = Favorite.objects.filter(customer = cust)
    faves = [product for fav in favorites for product in fav.favoriteproduct.all() if "DIY" not in product.name]

    favitems = False
    if favorites.exists():
        favitems = True
        
    return render(request, "webshop/favorites.html", {
        "favorites": faves,
        "favitems": favitems
    })

def info(request):
    return render(request, "webshop/information.html")

def query(request):

    if request.method == 'POST':

        query = request.POST.get('q')
        find_products = []

        for product in Product.objects.all():
            if query.lower() in product.name.lower() or product.name.lower() in query.lower() or query.lower() in product.description.lower():
                find_products.append(product)
        empty = False

        if not find_products:
            empty = True

        return render(request, "webshop/query.html", {
            "foundproducts": find_products,
            "empty": empty,
            "zoekterm": query
        })

    return redirect(home)

def discount(request):
    if request.method == "POST":
        # check if input is valid kortingscode
        pass
    return redirect(cart)