from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from .models import Book, Order, OrderItem
from drf_spectacular.utils import extend_schema_field
User=get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model=User
        fields=["id","name","email","username","password"]
        read_only_fields=["id"]
    def create(self,validated_data):
        password=validated_data.pop("password")
        return User.objects.create_user(password=password,role="customer",**validated_data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","name","email","role"]
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=["id","title","authors","genre","isbn","price","description","stock_quantity","image_url","created_at","updated_at"]
        read_only_fields=["id","created_at","updated_at"]
class OrderItemInputSerializer(serializers.Serializer):
    book_id=serializers.IntegerField(min_value=1)
    quantity=serializers.IntegerField(min_value=1)
class OrderCreateSerializer(serializers.Serializer):
    items=OrderItemInputSerializer(many=True,allow_empty=False)
    def validate_items(self,items):
        ids=[x["book_id"] for x in items]
        if len(ids)!=len(set(ids)): raise serializers.ValidationError("Each book may appear once; combine quantities.")
        return items
    @transaction.atomic
    def create(self,data):
        order=Order.objects.create(user=self.context["request"].user)
        total=0
        for item in data["items"]:
            try: book=Book.objects.select_for_update().get(pk=item["book_id"])
            except Book.DoesNotExist: raise serializers.ValidationError({"items":f"Book id {item['book_id']} does not exist."})
            qty=item["quantity"]
            if book.stock_quantity<qty: raise serializers.ValidationError({"items":f"Insufficient stock for {book.title}; available {book.stock_quantity}."})
            book.stock_quantity-=qty
            book.save(update_fields=["stock_quantity","updated_at"])
            OrderItem.objects.create(order=order,book=book,quantity=qty,unit_price=book.price)
            total+=book.price*qty
        order.total_amount=total
        order.save(update_fields=["total_amount","updated_at"])
        return order
class OrderItemSerializer(serializers.ModelSerializer):
    book_title=serializers.CharField(source="book.title",read_only=True)
    book_id=serializers.IntegerField(source="book.id",read_only=True)
    line_total=serializers.SerializerMethodField()
    class Meta:
        model=OrderItem
        fields=["book_id","book_title","quantity","unit_price","line_total"]
    @extend_schema_field(
        serializers.DecimalField(max_digits=12, decimal_places=2)
    )
    def get_line_total(self,obj): return obj.unit_price*obj.quantity
class OrderSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=["id","user","items","status","payment_status","total_amount","created_at","updated_at"]
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=["status","payment_status"]
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
