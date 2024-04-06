from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)    # Get the cart
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    cart = Cart(request)     # Get the Cart
    if request.POST.get('action') == 'post':   # 'POST' is post request from webpage ||  'post' is from AJAX action
        product_id = int(request.POST.get('product_id'))  # Get the product_id
        product_qty = int(request.POST.get('product_qty')) # Get the quantity of the product
        product = get_object_or_404(Product, id=product_id)  # Looking for the product in database
        cart.add(product = product, quantity = product_qty)   # Save to session
        cart_quantity = cart.__len__()  # Getting the cart quantity
        # Returning Response
        # response = JsonResponse({'Product Name: ' : product.name })
        response = JsonResponse({'qty' : cart_quantity })
        messages.success(request, ("Product added to the cart successfully"))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':   
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)  # calling delete function in cart
        response = JsonResponse({'product': product_id})
        messages.success(request, ("Product item has been removed from your cart . . ."))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':   
        product_id = int(request.POST.get('product_id')) 
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        # return redirect('cart_summary')
        messages.success(request, ("Your cart has been updated . . ."))
        return response