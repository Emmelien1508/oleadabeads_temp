from .models import Customer
from django.contrib.sessions.models import Session

def get_customer_session(request):

    request.session.clear_expired()

    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        request.session.create()
        s = Session.objects.get(pk=request.session.session_key)
    request.session.set_expiry(0)

    if request.user.is_anonymous:
        try:
            cust = Customer.objects.get(session = s)
        except:
            cust = Customer.objects.create()
            cust.session = s
            cust.save(update_fields=['session'])
    else:
        try:
            cust = Customer.objects.get(email = request.user.email, session = s)
        except:
            cust = Customer.objects.get(email = request.user.email)
            cust.session = s
            cust.save(update_fields=['session'])
    
    return cust