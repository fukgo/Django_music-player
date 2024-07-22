from django.urls import path
from . import views
app_name = 'user'
urlpatterns = [
    path('auth_code/', views.auth_code, name='auth_code'),
    path('login_out/', views.login_out, name='login_out'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/<int:id>', views.UserProfile.as_view(), name='profile'),

]

