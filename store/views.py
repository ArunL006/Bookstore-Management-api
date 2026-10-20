from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, Order
from .permissions import IsAdminOrReadOnly, IsAdminRole
from .serializers import RegisterSerializer, UserSerializer, BookSerializer, OrderCreateSerializer, OrderSerializer, OrderStatusSerializer
from drf_spectacular.utils import extend_schema
from .serializers import LoginSerializer, LoginResponseSerializer
User=get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[permissions.AllowAny]
class LoginView(APIView):
    permission_classes=[permissions.AllowAny]
    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginResponseSerializer},
    )
    def post(self,request):
        email=request.data.get("email","").strip().lower()
        user=authenticate(request,username=email,password=request.data.get("password",""))
        if not user: return Response({"error":"Invalid email or password."},status=status.HTTP_401_UNAUTHORIZED)
        refresh=RefreshToken.for_user(user)
        return Response({"access":str(refresh.access_token),"refresh":str(refresh),"user":UserSerializer(user).data})
class MeView(generics.RetrieveAPIView):
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self): return self.request.user
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "authors"]
    filterset_fields = ["genre"]
    ordering_fields = ["title", "price", "created_at"]
    ordering = ["title"]
class OrderViewSet(viewsets.ModelViewSet):
    http_method_names=["get","post","head","options"]
    serializer_class=OrderSerializer
    def get_queryset(self):
        qs=Order.objects.select_related("user").prefetch_related("items__book")
        if not self.request.user.is_authenticated: return qs.none()
        if self.request.user.is_staff or self.request.user.role=="admin": return qs
        return qs.filter(user=self.request.user)
    def get_permissions(self):
        return [permissions.IsAuthenticated()]
    def get_serializer_class(self):
        return OrderCreateSerializer if self.action=="create" else OrderSerializer
class OrderStatusView(APIView):
    permission_classes=[IsAdminRole]
    @extend_schema(
        request=OrderStatusSerializer,
        responses={200: OrderSerializer},
    )
    def patch(self,request,pk):
        try: order=Order.objects.get(pk=pk)
        except Order.DoesNotExist: return Response({"error":"Order not found."},status=404)
        serializer=OrderStatusSerializer(order,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)
