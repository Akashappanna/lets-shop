from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('products-<str:pk>', views.product, name='products'),
    path('delete-<str:pk>', views.deleteReview, name='deletereview'),
    path('cart/', views.cartPage, name='cart'),
    path('update-item/', views.updateItem, name='update-item'),
    path('delete-item/', views.deleteItem, name='delete-item'),
    path('aboutus', views.aboutUs, name='aboutus'),
    path('contact', views.contactUs, name='contact'),
]
