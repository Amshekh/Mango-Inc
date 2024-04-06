from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),     # always to be "login_user" to avoid name conflict
    path('logout/', views.logout_user, name='logout'),  # always to be "logout_user" to avoid name conflict
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'), # instead of 'cat' you may write any name
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
]
