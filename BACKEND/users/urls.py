from django.urls import path
from .views import login_view, register_view
from . import views
from django.contrib.auth.views import LogoutView
from .views import logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('logout/', logout_view, name='logout'),
]
