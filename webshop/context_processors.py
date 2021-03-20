from .utils import get_customer_session
from .models import *

def add_variable_to_context(request):
    try:
        cust = get_customer_session(request)
        items = OrderProduct.objects.filter(customer = cust, ordered=False)
        count = 0

        for item in items:
            count += item.quantity

    except:
        count = 0

    return {
        'cartnumber': count
    }