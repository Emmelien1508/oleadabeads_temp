from datetime import datetime 
from operator import itemgetter
from random import sample

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
    
    best = True
    if not bestsellers:
        best = False

    return bestsellers, best

def get_new_products():
    sorted_products = list(Product.objects.all().order_by("-date_added"))
    new_items = [product for product in sorted_products]

    if len(new_items) > 4:
        new_items = new_items[0:4]

    new = True
    if not new_items:
        new = False

    return new_items, new

def get_all_products(soort):
    products = [product for product in Product.objects.all() if product.jewelry_type == f"{soort.capitalize()}"]
    name = soort.capitalize()

    empty = False
    if not products:
        empty = True

    return products, name, empty

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

def get_all_cartitems(cust):
    products = []
    
    subtotal = 0
    messages = []
    for item in OrderProduct.objects.filter(customer = cust, ordered = False):
        if item.quantity > item.product.left:
            messages.append(f"Sorry, er zijn maar {item.product.left} stuk(s) beschikbaar van {item.product.name}!")
            item.quantity = item.product.left
            if item.product.sale:
                item.total = item.quantity * item.product.sale_price
            else:
                item.total = item.quantity * item.product.price
            item.save(update_fields=['quantity', 'total'])
        products.append(item)
        if item.product.sale:
            subtotal += item.quantity * item.product.sale_price
        else:
            subtotal += item.quantity * item.product.price

    incart = False
    if products:
        incart = True

    return products, incart, subtotal, messages

def add_product_to_cart(request, cust, item):
    amount = int(request.POST["hoeveelheid"])
    try:
        size = request.POST["size"]
    except:
        size = False

    try:
        cartproduct = OrderProduct.objects.get(customer = cust, product = item, ordered = False)
        cartproduct.quantity += amount
        if size:
            cartproduct.size = size

        if cartproduct.product.sale:
            cartproduct.total += amount * cartproduct.product.sale_price
        else:
            cartproduct.total += amount * cartproduct.product.price
        
        if size:
            cartproduct.save(update_fields=['quantity', 'total', 'size'])
        else:
            cartproduct.save(update_fields=['quantity', 'total'])
    except:
        cartproduct = OrderProduct()
        cartproduct.customer = cust
        cartproduct.product = item
        cartproduct.quantity = amount
        if size:
            cartproduct.size = size

        if cartproduct.product.sale:
            cartproduct.total = amount * cartproduct.product.sale_price
        else:
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

def create_order(cust, cart, subtotal, payment_option, shipping_option, comment):
    if subtotal > 35:
        freeshipping = True
        shipping_costs = 0
        total = subtotal
    else:
        freeshipping = False
        if "Brievenbuspakketje" in shipping_option:
            shipping_costs = 2
            total = subtotal + 2
        if "Met Track & Trace" in shipping_option:
            shipping_costs = 4
            total = subtotal + 4

    for item in cart:
        if item.product:
            item.product.left -= item.quantity
            if item.product.left == 0:
                item.product.in_stock = False
            item.product.save(update_fields=['left', 'in_stock'])

    order = Order.objects.create(customer = cust, date_ordered = datetime.now(), status = "Ontvangen", subtotal = subtotal, total = total, shipping = shipping_option, free_shipping = freeshipping, shipping_costs = shipping_costs, payment_option = payment_option, comment = comment)
    order.save()
    for item in cart:
        item.ordered = True
        item.save(update_fields=['ordered'])
        order.orderproduct.add(item)

    return order

def send_email(order, cust):
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

def get_random_products(item):
    products = list(Product.objects.exclude(id=item.id))
    random_products = sample(products, 4)
    return random_products