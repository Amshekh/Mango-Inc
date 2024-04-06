from django.contrib import admin
from . models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):   # Combine User Info and Profile Info
    model = Profile

class UserAdmin(admin.ModelAdmin):  # Extending User Model
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# Unregister the old way the User model was registered

admin.site.unregister(User)

# Re-register the User model in new way

admin.site.register(User, UserAdmin)