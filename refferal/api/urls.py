from django.urls import path

from api.views import (LoginAPIView, LoginAuthenticateAPIView,
                       UserProfileAPIView)

app_name = 'api'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login_authenticate/', LoginAuthenticateAPIView.as_view(), name='login_authenticate'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
