from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin para o modelo User customizado
    """
    # Campos exibidos na lista
    list_display = ['email', 'nome_completo', 'escolaridade', 'disciplina_preferida', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['escolaridade', 'disciplina_preferida', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'nome_completo', 'username']
    ordering = ['-date_joined']
    
    # Configuração dos fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'foto_perfil')}),
        ('Informações Acadêmicas', {'fields': ('escolaridade', 'disciplina_preferida')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos para adicionar usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'nome_completo', 'password1', 'password2', 'escolaridade', 'disciplina_preferida'),
        }),
    )
