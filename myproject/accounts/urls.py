from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticação
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Perfil do usuário
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('dashboard/', views.user_dashboard_view, name='dashboard'),
    
    # Administração (opcional)
    path('users/', views.UserListView.as_view(), name='user_list'),
]