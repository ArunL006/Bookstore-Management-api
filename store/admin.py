
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Order, OrderItem


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "name",
        "role",
        "is_staff",
        "is_active",
    )

    # Extend existing fieldsets without duplicating email.
    fieldsets = UserAdmin.fieldsets + (
        ("Store Profile", {"fields": ("name", "role")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Store Profile",
            {"fields": ("name", "role", "email")},
        ),
    )

    ordering = ("email",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "authors",
        "genre",
        "price",
        "stock_quantity",
    )
    search_fields = ("title", "authors", "isbn")
    list_filter = ("genre",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "payment_status",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "payment_status")
    inlines = [OrderItemInline]
