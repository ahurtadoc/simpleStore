from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy', views.buy),
    path('buy/<int:order_id>', views.resume),
    path('pay/<int:order_id>', views.pay),
    path('state/<int:order_id>', views.order_state)
]
