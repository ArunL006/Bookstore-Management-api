from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, OrderViewSet, OrderStatusView
router=DefaultRouter()
router.register("books",BookViewSet,basename="book")
router.register("orders",OrderViewSet,basename="order")
urlpatterns=[path("",include(router.urls)),path("orders/<int:pk>/status/",OrderStatusView.as_view(),name="order-status")]
