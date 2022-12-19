from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
#from .products import products
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from app.models import Product, Order
from .serializer import ProductSerializer, UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, filters, generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.contrib.auth.hashers import make_password
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

API_URL = "http/locahost:8000"


@api_view(['GET'])
def getRoutes(request):
    return Response('hello')


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProductFilter(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

# Register new users


@api_view(['POST'])
def registerUser(request):
    try:
        data = request.data
        print(data)
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']),
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'details': 'USER WITH THIS EMAIL ALREADY EXITS!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
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
                success_url=settings.SITE_URL +
                '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/' + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# custom payment flow
class CreatePaymentIntent(APIView):
    def post(self, request, *args, **kwargs):
        prod_id = request.data
        product = Product.objects.get(id=prod_id)
        try:
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
            return Response({'clientSecret': intent['client_secret']}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=400)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']

        print(intent)
        payment_intent = intent.charges.data[0]
        # customer_email=session['customer_details']['email']
        prod_id = payment_intent['metadata']['product_id']
        product = Product.objects.get(id=prod_id)

        # #creating payment history
        # # user=User.objects.get(email=customer_email) or None

        Order.objects.create(product=product, payment_status=True)
    # Passed signature verification
    return HttpResponse(status=200)
