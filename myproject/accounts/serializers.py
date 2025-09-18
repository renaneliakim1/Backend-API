from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de novos usuários
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'nome_completo', 'password', 'password_confirm',
            'escolaridade', 'disciplina_preferida', 'foto_perfil'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'nome_completo': {'required': True},
            'escolaridade': {'required': True},
            'disciplina_preferida': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para dados do usuário (leitura e atualização)
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'nome_completo', 'escolaridade',
            'disciplina_preferida', 'foto_perfil', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'email', 'username', 'date_joined', 'last_login']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização do perfil do usuário
    """
    class Meta:
        model = User
        fields = ['nome_completo', 'escolaridade', 'disciplina_preferida', 'foto_perfil']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer para mudança de senha
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuários
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,  # Como definimos email como USERNAME_FIELD
                password=password
            )
            
            if not user:
                raise serializers.ValidationError('Email ou senha inválidos.')
            
            if not user.is_active:
                raise serializers.ValidationError('Conta desativada.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')