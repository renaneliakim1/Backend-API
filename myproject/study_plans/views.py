from django.shortcuts import render
from rest_framework import generics, viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime, date
from .models import Disciplina, PlanoEstudo, AtividadePlano, ProgressoUsuario
from .serializers import (
    DisciplinaSerializer, PlanoEstudoSerializer, PlanoEstudoCreateSerializer,
    AtividadePlanoSerializer, ProgressoUsuarioSerializer, PlanoEstudoResumoSerializer
)


class DisciplinaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para disciplinas (apenas leitura)
    """
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsAuthenticated]


class PlanoEstudoViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para planos de estudo
    """
    serializer_class = PlanoEstudoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PlanoEstudo.objects.filter(usuario=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PlanoEstudoCreateSerializer
        elif self.action == 'list':
            return PlanoEstudoResumoSerializer
        return PlanoEstudoSerializer
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """
        Ativar um plano de estudos
        """
        plano = self.get_object()
        plano.status = 'active'
        plano.data_inicio = date.today()
        plano.save()
        
        return Response({
            'message': 'Plano ativado com sucesso!',
            'plano': PlanoEstudoSerializer(plano, context={'request': request}).data
        })
    
    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        """
        Concluir um plano de estudos
        """
        plano = self.get_object()
        plano.status = 'completed'
        plano.data_fim_real = date.today()
        plano.save()
        
        return Response({
            'message': 'Plano concluído com sucesso!',
            'plano': PlanoEstudoSerializer(plano, context={'request': request}).data
        })
    
    @action(detail=True, methods=['get'])
    def atividades_semana(self, request, pk=None):
        """
        Obter atividades de uma semana específica
        """
        plano = self.get_object()
        semana = request.query_params.get('semana', 1)
        
        atividades = plano.atividades.filter(semana=semana).order_by('dia_semana', 'ordem')
        serializer = AtividadePlanoSerializer(atividades, many=True)
        
        return Response({
            'semana': semana,
            'atividades': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        """
        Obter estatísticas do plano
        """
        plano = self.get_object()
        total_atividades = plano.atividades.count()
        atividades_concluidas = plano.atividades.filter(
            progressos__usuario=request.user,
            progressos__concluida=True
        ).count()
        
        tempo_total_estimado = sum(
            atividade.tempo_estimado_minutos 
            for atividade in plano.atividades.all()
        )
        
        tempo_gasto_real = sum(
            progresso.tempo_gasto_minutos or 0
            for progresso in ProgressoUsuario.objects.filter(
                usuario=request.user,
                atividade__plano=plano,
                concluida=True
            )
        )
        
        return Response({
            'total_atividades': total_atividades,
            'atividades_concluidas': atividades_concluidas,
            'progresso_percentual': round((atividades_concluidas / total_atividades * 100) if total_atividades > 0 else 0, 2),
            'tempo_total_estimado_horas': round(tempo_total_estimado / 60, 2),
            'tempo_gasto_real_horas': round(tempo_gasto_real / 60, 2),
        })


class AtividadePlanoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para atividades dos planos
    """
    serializer_class = AtividadePlanoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AtividadePlano.objects.filter(plano__usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def marcar_concluida(self, request, pk=None):
        """
        Marcar uma atividade como concluída
        """
        atividade = self.get_object()
        
        progresso, created = ProgressoUsuario.objects.get_or_create(
            usuario=request.user,
            atividade=atividade,
            defaults={
                'concluida': True,
                'data_conclusao': datetime.now(),
                'tempo_gasto_minutos': request.data.get('tempo_gasto_minutos'),
                'nota_auto_avaliacao': request.data.get('nota_auto_avaliacao'),
                'observacoes': request.data.get('observacoes', '')
            }
        )
        
        if not created:
            progresso.concluida = True
            progresso.data_conclusao = datetime.now()
            progresso.tempo_gasto_minutos = request.data.get('tempo_gasto_minutos')
            progresso.nota_auto_avaliacao = request.data.get('nota_auto_avaliacao')
            progresso.observacoes = request.data.get('observacoes', '')
            progresso.save()
        
        return Response({
            'message': 'Atividade marcada como concluída!',
            'progresso': ProgressoUsuarioSerializer(progresso).data
        })


class ProgressoUsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para progresso do usuário
    """
    serializer_class = ProgressoUsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProgressoUsuario.objects.filter(usuario=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_estatisticas(request):
    """
    Estatísticas gerais para o dashboard
    """
    user = request.user
    
    # Planos
    total_planos = PlanoEstudo.objects.filter(usuario=user).count()
    planos_ativos = PlanoEstudo.objects.filter(usuario=user, status='active').count()
    planos_concluidos = PlanoEstudo.objects.filter(usuario=user, status='completed').count()
    
    # Atividades
    total_atividades = AtividadePlano.objects.filter(plano__usuario=user).count()
    atividades_concluidas = ProgressoUsuario.objects.filter(
        usuario=user, 
        concluida=True
    ).count()
    
    # Tempo de estudo
    tempo_total_estudado = sum(
        progresso.tempo_gasto_minutos or 0
        for progresso in ProgressoUsuario.objects.filter(
            usuario=user,
            concluida=True
        )
    )
    
    # Progressos recentes
    progressos_recentes = ProgressoUsuario.objects.filter(
        usuario=user,
        concluida=True
    ).order_by('-data_conclusao')[:5]
    
    return Response({
        'planos': {
            'total': total_planos,
            'ativos': planos_ativos,
            'concluidos': planos_concluidos,
        },
        'atividades': {
            'total': total_atividades,
            'concluidas': atividades_concluidas,
            'percentual': round((atividades_concluidas / total_atividades * 100) if total_atividades > 0 else 0, 2)
        },
        'tempo_estudado_horas': round(tempo_total_estudado / 60, 2),
        'progressos_recentes': ProgressoUsuarioSerializer(progressos_recentes, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gerar_plano_ia(request):
    """
    Endpoint para gerar plano de estudos usando IA (placeholder)
    """
    # Por enquanto, este é um placeholder
    # Futuramente aqui será integrada a IA para gerar planos personalizados
    
    dados = request.data
    
    # Validações básicas
    required_fields = ['objetivos', 'disciplinas_ids', 'tempo_disponivel', 'nivel_dificuldade']
    for field in required_fields:
        if field not in dados:
            return Response(
                {'error': f'Campo {field} é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Simular resposta da IA (substituir por integração real)
    plano_sugerido = {
        'titulo': f"Plano de {dados['objetivos']}",
        'descricao': f"Plano personalizado baseado em seus objetivos: {dados['objetivos']}",
        'nivel_dificuldade': dados['nivel_dificuldade'],
        'horas_por_semana': dados.get('horas_por_semana', 10),
        'duracao_semanas': dados.get('duracao_semanas', 8),
        'disciplinas_ids': dados['disciplinas_ids'],
        'objetivos': dados['objetivos'],
        'tempo_disponivel': dados['tempo_disponivel'],
        'conhecimento_previo': dados.get('conhecimento_previo', ''),
    }
    
    # Criar o plano usando o serializer
    serializer = PlanoEstudoCreateSerializer(
        data=plano_sugerido,
        context={'request': request}
    )
    
    if serializer.is_valid():
        plano = serializer.save()
        return Response({
            'message': 'Plano gerado com sucesso!',
            'plano': PlanoEstudoSerializer(plano, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
