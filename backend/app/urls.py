from django.urls import path
from app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
path('', views.getRoutes, name="get-routes"),
path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('products/', views.getProducts, name="get-products"),
path('products/<str:pk>', views.getProduct, name="get-product"),
path('user/profile/', views.getUserProfile, name="get-user-profile"),
path('users/', views.getUsers, name="get-users"),
]