from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from django.conf import settings
import stripe

from app.models import Product, Order
from .serializer import ProductSerializer, UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['GET'])
def getRoutes(request):
    """
    Endpoint to retrieve available API routes.
    """
    routes = {
        'products': '/api/products/',
        'product-detail': '/api/products/<id>/',
        'users': '/api/users/',
        'user-profile': '/api/users/profile/',
        'register': '/api/users/register/',
        'token': '/api/token/',
        'stripe-checkout': '/api/stripe/checkout/',
        'stripe-webhook': '/api/stripe/webhook/',
    }
    return Response(routes)


@api_view(['GET'])
def getProducts(request):
    """
    Endpoint to fetch all products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    """
    Endpoint to fetch a specific product by id.
    """
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer to include additional user data.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view to use MyTokenObtainPairSerializer.
    """
    serializer_class = MyTokenObtainPairSerializer


class ProductFilter(generics.ListCreateAPIView):
    """
    API view to list and filter products by name.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    """
    Endpoint to retrieve the current user's profile.
    """
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    """
    Endpoint to retrieve all users (admin only).
    """
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    """
    Endpoint to register a new user.
    """
    try:
        data = request.data
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']),
        )
        serializer = UserSerializerWithToken(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_id(request, pk):
    """
    Endpoint to retrieve a user by id (admin only).
    """
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    """
    Endpoint to handle Stripe checkout session creation.
    """
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'currency': 'usd',
                        'price': 'price_1MAtSLJU3RVFqD4TnNYWOxPO',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreatePaymentIntent(APIView):
    """
    Endpoint to create a Stripe payment intent.
    """
    def post(self, request):
        prod_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=prod_id)
            intent = stripe.PaymentIntent.create(
                amount=int(product.price) * 100,
                currency='usd',
                automatic_payment_methods={
                    'enabled': True,
                },
                metadata={
                    'product_id': product.id
                }
            )
            return Response({'clientSecret': intent['client_secret']}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def stripe_webhook_view(request):
    """
    Endpoint to handle Stripe webhook events.
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        prod_id = intent['metadata']['product_id']
        try:
            product = Product.objects.get(id=prod_id)
            Order.objects.create(product=product, payment_status=True)
        except Product.DoesNotExist:
            pass  # Handle case where product doesn't exist

    return HttpResponse(status=status.HTTP_200_OK)
