from django.db import models
from django.conf import settings


class Disciplina(models.Model):
    """
    Modelo para representar disciplinas disponíveis
    """
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class PlanoEstudo(models.Model):
    """
    Modelo para representar um plano de estudos personalizado
    """
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('active', 'Ativo'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]
    
    DIFICULDADE_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planos_estudo'
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    disciplinas = models.ManyToManyField(Disciplina, related_name='planos')
    
    # Configurações do plano
    nivel_dificuldade = models.CharField(
        max_length=20,
        choices=DIFICULDADE_CHOICES,
        default='iniciante'
    )
    horas_por_semana = models.PositiveIntegerField(help_text="Horas de estudo por semana")
    duracao_semanas = models.PositiveIntegerField(help_text="Duração do plano em semanas")
    
    # Status e controle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    data_inicio = models.DateField(null=True, blank=True)
    data_fim_prevista = models.DateField(null=True, blank=True)
    data_fim_real = models.DateField(null=True, blank=True)
    
    # Geração por IA
    gerado_por_ia = models.BooleanField(default=True)
    prompt_usado = models.TextField(blank=True, help_text="Prompt usado para gerar o plano")
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Plano de Estudo"
        verbose_name_plural = "Planos de Estudo"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.nome_completo}"


class AtividadePlano(models.Model):
    """
    Modelo para representar atividades dentro de um plano de estudos
    """
    TIPO_CHOICES = [
        ('leitura', 'Leitura'),
        ('exercicio', 'Exercício'),
        ('video', 'Vídeo'),
        ('pratica', 'Prática'),
        ('revisao', 'Revisão'),
        ('avaliacao', 'Avaliação'),
    ]
    
    plano = models.ForeignKey(
        PlanoEstudo,
        on_delete=models.CASCADE,
        related_name='atividades'
    )
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    # Organização
    semana = models.PositiveIntegerField(help_text="Semana do plano")
    dia_semana = models.PositiveIntegerField(help_text="Dia da semana (1-7)")
    ordem = models.PositiveIntegerField(help_text="Ordem da atividade no dia")
    
    # Tempo estimado
    tempo_estimado_minutos = models.PositiveIntegerField(help_text="Tempo estimado em minutos")
    
    # Recursos
    recursos_necessarios = models.TextField(blank=True, help_text="Materiais ou recursos necessários")
    links_uteis = models.JSONField(default=list, blank=True, help_text="Links úteis para a atividade")
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Atividade do Plano"
        verbose_name_plural = "Atividades do Plano"
        ordering = ['semana', 'dia_semana', 'ordem']
    
    def __str__(self):
        return f"{self.titulo} - Semana {self.semana}"


class ProgressoUsuario(models.Model):
    """
    Modelo para acompanhar o progresso do usuário nas atividades
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progressos'
    )
    atividade = models.ForeignKey(
        AtividadePlano,
        on_delete=models.CASCADE,
        related_name='progressos'
    )
    
    concluida = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    tempo_gasto_minutos = models.PositiveIntegerField(null=True, blank=True)
    nota_auto_avaliacao = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Nota de 1 a 5 que o usuário se dá"
    )
    observacoes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Progresso do Usuário"
        verbose_name_plural = "Progressos dos Usuários"
        unique_together = ['usuario', 'atividade']
    
    def __str__(self):
        status = "Concluída" if self.concluida else "Pendente"
        return f"{self.atividade.titulo} - {self.usuario.nome_completo} ({status})"
