from datetime import datetime 
from operator import itemgetter

from .models import *

from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def get_customer_session(request):
    if not request.session or not request.session.session_key:
        request.session.save()

    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        s = Session.objects.create(pk=request.session.session_key)

    if not request.user.is_anonymous:
        try:
            cust = Customer.objects.get(email = request.user.email, session = s)
        except:
            cust = Customer.objects.get(email = request.user.email)
            cust.session = s
            cust.save(update_fields=['session'])

        all_customers = Customer.objects.filter(session = s)
        if len(all_customers) > 1:
            head_cust = all_customers[0]
            temp_cust = all_customers[1]
            for customer in all_customers:
                if not customer.email:
                    try:
                        obj = OrderProduct.objects.filter(customer = temp_cust)
                    except:
                        pass
                    
                    for op in obj:
                        op.customer = head_cust
                        op.save(update_fields=['customer'])
                    customer.delete()
            del temp_cust
    else:
        try:
            cust = Customer.objects.get(session = s)
        except:
            cust = Customer.objects.create(session = s)

    return cust

def get_sorted_bestsellers():
    sold_items = OrderProduct.objects.filter(ordered=True).order_by("product")
    products = {}

    for item in sold_items:
        try:
            products[item.product.name] += item.quantity
        except:
            products[item.product.name] = item.quantity

    sorted_bestsellers = dict(sorted(products.items(), key=itemgetter(1),reverse=True))
    bestsellers = [product for title in sorted_bestsellers.keys() for product in Product.objects.all() if product.name == title]

    if len(bestsellers) > 4:
        bestsellers = bestsellers[0:4]
    
    best = True
    if not bestsellers:
        best = False

    return bestsellers, best

def get_all_products(soort):
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
        sorted_bestsellers = dict(sorted(bestsellers.items(), key=itemgetter(1),reverse=True))
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

    return products, text, name, empty

def get_product_info(cust, naam):
    item = Product.objects.get(name=naam)
    outofstock = True
    if item.in_stock:
        outofstock = False

    images = [img for img in item.image.all()]
    
    try:
        fav = Favorite.objects.get(customer = cust, favoriteproduct = item)
        added = True
    except:
        added = False

    try:
        cartitem = OrderProduct.objects.get(customer = cust, product = item)
        incart = True
    except:
        incart = False

    return item, outofstock, added, incart, images

def save_diy_data(request):
    jewelrytype = request.POST['jewelrytype']
    look = request.POST['look']
    color = request.POST.getlist('color[]')
    colors = []
    for c in color:
        if '€' in c:
            colors.append(c[:-10])
        else:
            colors.append(c)
    chosencolors = [Color.objects.get(color = col) for col in colors]
    metaltype = request.POST['metaltype']

    return jewelrytype, look, chosencolors, metaltype

def create_diy_product(jewelrytype, look, colors, metaltype):
    price = 5
    if "Ketting" in jewelrytype:
        price += 2
    if "Schakelketting" in look:
        price += 1.50
    if "Edelsteen" in colors:
        price += 1.50
    if "Parel" in colors:
        price += 1
    if "Goud" in metaltype:
        price += 0.5

    diy = Diy.objects.create(price = price, jewelry_type = jewelrytype, look = look, metal_type = metaltype)
    diy.name = str(diy.id)
    diy.save(update_fields=['name'])
    diy.color.set(colors)

    return diy

def create_diy_cartitem(diy, cust):
    cartproduct = OrderProduct()
    cartproduct.diyproduct = diy
    cartproduct.customer = cust
    cartproduct.total = cartproduct.diyproduct.price
    cartproduct.quantity = 1
    cartproduct.save()

def get_all_cartitems(cust):
    diyproducts, normalproducts = [], []
    
    total = 0
    for item in OrderProduct.objects.filter(customer = cust, ordered = False):
        if item.product:
            if item.quantity > item.product.left:
                item.quantity = item.product.left
                item.total = item.quantity * item.product.price
                item.save(update_fields=['quantity', 'total'])
            normalproducts.append(item)
            total += item.quantity * item.product.price
        else:
            diyproducts.append(item)
            total += item.quantity * item.diyproduct.price

    incart = False
    if diyproducts or normalproducts:
        incart = True

    return diyproducts, normalproducts, incart, total

def add_product_to_cart(request, cust, item):
    amount = int(request.POST["hoeveelheid"])
    try:
        cartproduct = OrderProduct.objects.get(customer = cust, product = item, ordered = False)
        cartproduct.quantity += amount
        cartproduct.total += amount * cartproduct.product.price
        cartproduct.save(update_fields=['quantity', 'total'])
    except:
        cartproduct = OrderProduct()
        cartproduct.customer = cust
        cartproduct.product = item
        cartproduct.quantity = amount
        cartproduct.total = amount * cartproduct.product.price
        cartproduct.save()
        
def save_checkout_data(request, cust):
    straat = request.POST['streetname']
    huisnr = request.POST['housenr']
    postcode = request.POST['postalcode']
    stad = request.POST['city']
    betaalwijze = request.POST['payment_option']
    verzendmethode = request.POST['shipping_option']
    opmerkingen = request.POST['comments']
    voornaam = request.POST['voornaam']
    achternaam = request.POST['achternaam']
    email = request.POST['email']

    if request.user.is_anonymous:
        cust.firstname = voornaam
        cust.lastname = achternaam
        cust.email = email

    cust.streetname = straat
    cust.housenr = huisnr
    cust.postalcode = postcode
    cust.city = stad

    cust.save(update_fields=['email', 'firstname', 'lastname', 'streetname', 'housenr', 'postalcode', 'city'])
    
    return OrderProduct.objects.filter(customer = cust, ordered = False), betaalwijze, verzendmethode, opmerkingen

def create_order(cust, cart, total, payment_option, shipping_option, comment):
    if total > 35:
        freeshipping = True
    else:
        freeshipping = False
        if "Brievenbuspakketje" in shipping_option:
            total += 2
        if "Met Track & Trace" in shipping_option:
            total += 4

    for item in cart:
        if item.product:
            item.product.left -= item.quantity
            item.product.save(update_fields=['left'])

    order = Order.objects.create(customer = cust, date_ordered = datetime.now(), status = "Ontvangen", total = total, shipping = shipping_option, free_shipping = freeshipping, payment_option = payment_option, comment = comment)
    order.save()
    for item in cart:
        item.ordered = True
        item.save(update_fields=['ordered'])
        order.orderproduct.add(item)

    return order

def send_email(order, cust, shipping_option):
    context = {
        "order": order,
        "customer": cust,
        "shipping": shipping_option
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

def get_favorite_info(cust):    
    favorites = Favorite.objects.filter(customer = cust)
    faves = [product for fav in favorites for product in fav.favoriteproduct.all()]

    favitems = False
    if faves:
        favitems = True

    return faves, favitems

def process_discount(discount, cust, total):
    if discount.discount_type == "Vast bedrag":
        minus = discount.discount_amount
        total -= minus
    else:
        minus = discount.discount_percentage / 100
        total *= (1 - minus)

    return total

def change_profile_info(request, cust):
    straat = request.POST['streetname']
    huisnr = request.POST['housenr']
    postcode = request.POST['postalcode']
    stad = request.POST['city']
    voornaam = request.POST['voornaam']
    achternaam = request.POST['achternaam']
    email = request.POST['email']

    cust.firstname = voornaam
    cust.lastname = achternaam
    cust.email = email
    cust.streetname = straat
    cust.housenr = huisnr
    cust.postalcode = postcode
    cust.city = stad

    cust.save(update_fields=['email', 'firstname', 'lastname', 'streetname', 'housenr', 'postalcode', 'city'])

def send_update_email(order):
    context = {
        "order": order
    }

    subject = f"Dankjewel voor je bestelling {order.customer.firstname}!"
    msg_plain = render_to_string("webshop/update_email.txt", context)
    msg_html = render_to_string("webshop/update_email.html", context)
    from_email = settings.EMAIL_HOST_USER
    to_list = [f"{order.customer.email}"]

    send_mail(
        subject,
        msg_plain,
        from_email,
        to_list,
        html_message=msg_html,
        fail_silently=True,
    )