from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.get_items, name='get_items'),
    path('order/<int:item_id>/', views.order_item, name='order_item'),
]
