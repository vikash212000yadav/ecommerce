from user.views import UserView, UserCreateView, SellerCreateView, DeliveryInfoView, ChangePasswordView, \
    session_auth_view
from django.urls import path

urlpatterns = [
    path('user/$', UserView.as_view(), name='user'),
    path('user/create/$', UserCreateView.as_view(), name='user-create'),
    path('seller/create/$', SellerCreateView.as_view(), name='seller-create'),
    path('deliveryinfo/$', DeliveryInfoView.as_view(), name='delivery-info'),
    path('auth/$', session_auth_view, name='auth'),
    path('password/$', ChangePasswordView.as_view(), name='change-password'),
]