from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    ProductFilter, StripeCheckoutView, getRoutes, registerUser,
    getProducts, getProduct, getUserProfile, getUsers, get_user_by_id
)

urlpatterns = [
    path('', getRoutes, name="get-routes"),
    path('users/register/', registerUser, name="register"),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('products/', getProducts, name="get-products"),
    path('products/<str:pk>', getProduct, name="get-product"),
    path('user/profile/', getUserProfile, name="get-user-profile"),
    path('users/', getUsers, name="get-users"),
    path('users/<str:pk>/', get_user_by_id, name='get-user-id'),
    path('products/search/', ProductFilter.as_view(), name="search-product"),
    path('create-checkout-session/<str:pk>/',
         csrf_exempt(StripeCheckoutView.as_view()), name='checkout_session'),
]
