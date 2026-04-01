from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import EmailTokenObtainView

urlpatterns = [
    path('login', EmailTokenObtainView.as_view(), name='email_login'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh')
]