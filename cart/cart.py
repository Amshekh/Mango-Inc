from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')  # case 1: Getting the existing current session key 

        if 'session_key' not in request.session: # case 2: User is new so you need to create a new session key
            cart = self.session['session_key'] = {}


        self.cart = cart    # To make sure that cart is available on all pages of your web application    


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:  # Logged in user
            current_user = Profile.objects.filter(user__id=self.request.user.id)  # Get Profile of current user
            cart_str = str(self.cart)    # typecasting or converting python dictionary to string
            cart_str = cart_str.replace("\'", "\"")    # replacing single quation with double quotation for it to be JSON format
            current_user.update(previous_cart=str(cart_str))  # Save cart_str to Profile model

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:  # Logged in user
            current_user = Profile.objects.filter(user__id=self.request.user.id)  # Get Profile of current user
            cart_str = str(self.cart)    # typecasting or converting python dictionary to string
            cart_str = cart_str.replace("\'", "\"")    # replacing single quation with double quotation for it to be JSON format
            current_user.update(previous_cart=str(cart_str))  # Save cart_str to Profile model

    def cart_total(self):
        product_ids = self.cart.keys()  # Get product IDS
        products = Product.objects.filter(id__in=product_ids) # looking up in our Product model
        quantities = self.cart
        total = 0   # Counting starts from 0

        for key, value in quantities.items():
            key = int(key)  # Converting from string to integer (Typecasting)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total            

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()  # Getting id's of the product from cart
        products = Product.objects.filter(id__in=product_ids)   # Using id's to lookup product in database model

        return products   # Return those looked up products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart  # Get cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:  # Logged in user
            current_user = Profile.objects.filter(user__id=self.request.user.id)  # Get Profile of current user
            cart_str = str(self.cart)    # typecasting or converting python dictionary to string
            cart_str = cart_str.replace("\'", "\"")    # replacing single quation with double quotation for it to be JSON format
            current_user.update(previous_cart=str(cart_str))  # Save cart_str to Profile model

        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:    # Delete from dictionary/cart
            del self.cart[product_id]

        self.session.modified = True   

        if self.request.user.is_authenticated:  # Logged in user
            current_user = Profile.objects.filter(user__id=self.request.user.id)  # Get Profile of current user
            cart_str = str(self.cart)    # typecasting or converting python dictionary to string
            cart_str = cart_str.replace("\'", "\"")    # replacing single quation with double quotation for it to be JSON format
            current_user.update(previous_cart=str(cart_str))  # Save cart_str to Profile model 