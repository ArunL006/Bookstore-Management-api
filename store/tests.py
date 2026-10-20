from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book,User,Order
class BookstoreTests(APITestCase):
    def setUp(self):
        self.book=Book.objects.create(title="Django Basics",authors="A Writer",genre="Technology",isbn="9781234567890",price=Decimal("250.00"),stock_quantity=5)
        self.customer=User.objects.create_user(username="reader",email="reader@example.com",name="Reader",password="StrongPass123!",role="customer")
        self.admin=User.objects.create_user(username="manager",email="admin@example.com",name="Manager",password="StrongPass123!",role="admin",is_staff=True)
    def login(self,user):
        r=self.client.post("/api/login/",{"email":user.email,"password":"StrongPass123!"},format="json")
        self.assertEqual(r.status_code,200)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+r.data["access"])
    def test_public_book_list(self):
        r=self.client.get("/api/books/")
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.data["count"],1)
    def test_customer_cannot_create_book(self):
        self.login(self.customer)
        r=self.client.post("/api/books/",{"title":"Nope"},format="json")
        self.assertEqual(r.status_code,403)
    def test_admin_can_create_book(self):
        self.login(self.admin)
        r=self.client.post("/api/books/",{"title":"New Book","authors":"Author","genre":"Fiction","isbn":"9780000000002","price":"99.00","stock_quantity":3},format="json")
        self.assertEqual(r.status_code,201)
    def test_order_decrements_stock(self):
        self.login(self.customer)
        r=self.client.post("/api/orders/",{"items":[{"book_id":self.book.id,"quantity":2}]},format="json")
        self.assertEqual(r.status_code,201)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock_quantity,3)
    def test_insufficient_stock_rejected(self):
        self.login(self.customer)
        r=self.client.post("/api/orders/",{"items":[{"book_id":self.book.id,"quantity":99}]},format="json")
        self.assertEqual(r.status_code,400)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock_quantity,5)
    def test_customer_only_sees_own_orders(self):
        self.login(self.customer)
        self.client.post("/api/orders/",{"items":[{"book_id":self.book.id,"quantity":1}]},format="json")
        self.assertEqual(self.client.get("/api/orders/").data["count"],1)
    
    def test_customer_cannot_update_book(self):
        self.login(self.customer)
        response = self.client.patch(
            f"/api/books/{self.book.id}/",
            {"description": "Unauthorized change"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.book.refresh_from_db()
        self.assertNotEqual(self.book.description, "Unauthorized change")

    def test_customer_cannot_delete_book(self):
        self.login(self.customer)
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book.id).exists())

    def test_admin_can_update_book(self):
        self.login(self.admin)
        response = self.client.patch(
            f"/api/books/{self.book.id}/",
            {"description": "Updated by admin"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()
        self.assertEqual(self.book.description, "Updated by admin")

