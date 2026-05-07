from django.urls import path
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('userlist/',views.userlist,name='userlist'),
    path('deleteuser/<int:id>/',views.deleteuser,name='deleteuser'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('products/',views.product,name='products'),
    path('productlist/', views.product_list, name='productlist'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'), 
    path('userproductlist/', views.userproduct_list, name='userproductlist'),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('viewwishlist/', views.viewwishlist, name='viewwishlist'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

]