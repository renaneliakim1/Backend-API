from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileUpdateSerializer,
    PasswordChangeSerializer, LoginSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    View para registro de novos usuários
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuário criado com sucesso!',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    View para login de usuários
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'Login realizado com sucesso!',
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    View para logout (blacklist do token)
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout realizado com sucesso!'})
    except Exception as e:
        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View para visualizar e atualizar perfil do usuário
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    View para mudança de senha
    """
    serializer = PasswordChangeSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Senha alterada com sucesso!'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    View para listar usuários (apenas para admins)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Apenas admins podem ver a lista de usuários
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.none()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_view(request):
    """
    View para dados do dashboard do usuário
    """
    user = request.user
    
    # Estatísticas básicas do usuário
    total_planos = user.planos_estudo.count()
    planos_ativos = user.planos_estudo.filter(status='active').count()
    planos_concluidos = user.planos_estudo.filter(status='completed').count()
    
    # Progresso recente
    progressos_recentes = user.progressos.filter(concluida=True).order_by('-data_conclusao')[:5]
    
    return Response({
        'user': UserSerializer(user).data,
        'estatisticas': {
            'total_planos': total_planos,
            'planos_ativos': planos_ativos,
            'planos_concluidos': planos_concluidos,
        },
        'progressos_recentes': len(progressos_recentes),  # Simplified for now
    })
