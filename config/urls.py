from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from store.views import RegisterView, LoginView, MeView
from django.http import JsonResponse
urlpatterns = [
 path("admin/",admin.site.urls), path("api/register/",RegisterView.as_view()),
 path("api/login/",LoginView.as_view()), path("api/token/refresh/",TokenRefreshView.as_view()),
 path("api/me/",MeView.as_view()), path("api/",include("store.urls")),
 path("api/schema/",SpectacularAPIView.as_view(),name="schema"),
 path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
 path("api/redoc/",SpectacularRedocView.as_view(url_name="schema"),name="redoc"),
 path("", lambda request: JsonResponse({
    "message": "Welcome to Bookstore Management API",
    "docs": "/api/docs/",
    "books": "/api/books/"
})),
]
