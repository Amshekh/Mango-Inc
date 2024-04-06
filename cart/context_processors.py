from .cart import Cart

def cart(request):      # For cart to work on all pages of web-application, i'm creating context-processors
    return {'cart': Cart(request)}  # Default data from our cart is returned