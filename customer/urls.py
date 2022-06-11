from django.urls import path
from . import views

app_name='customer'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'),  #https://docs.djangoproject.com/en/4.0/topics/http/urls/
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),
]
