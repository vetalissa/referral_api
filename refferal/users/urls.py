from django.urls import path

from users.views import login, login_authenticate, logout_view, user_profile

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('login_authenticate/', login_authenticate, name='login_authenticate'),
    path('profile/', user_profile, name='profile'),
    path('logout/', logout_view, name='logout'),
]
