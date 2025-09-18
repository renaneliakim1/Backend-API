from django.contrib import admin
from .models import Disciplina, PlanoEstudo, AtividadePlano, ProgressoUsuario


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'created_at']
    search_fields = ['nome']
    ordering = ['nome']


class AtividadePlanoInline(admin.TabularInline):
    model = AtividadePlano
    extra = 0
    fields = ['titulo', 'disciplina', 'tipo', 'semana', 'dia_semana', 'tempo_estimado_minutos']


@admin.register(PlanoEstudo)
class PlanoEstudoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'status', 'nivel_dificuldade', 'horas_por_semana', 'created_at']
    list_filter = ['status', 'nivel_dificuldade', 'gerado_por_ia', 'created_at']
    search_fields = ['titulo', 'usuario__nome_completo', 'usuario__email']
    filter_horizontal = ['disciplinas']
    inlines = [AtividadePlanoInline]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'usuario', 'disciplinas')
        }),
        ('Configurações', {
            'fields': ('nivel_dificuldade', 'horas_por_semana', 'duracao_semanas')
        }),
        ('Status', {
            'fields': ('status', 'data_inicio', 'data_fim_prevista', 'data_fim_real')
        }),
        ('IA', {
            'fields': ('gerado_por_ia', 'prompt_usado'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AtividadePlano)
class AtividadePlanoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'plano', 'disciplina', 'tipo', 'semana', 'dia_semana', 'tempo_estimado_minutos']
    list_filter = ['tipo', 'disciplina', 'semana']
    search_fields = ['titulo', 'plano__titulo']
    ordering = ['plano', 'semana', 'dia_semana', 'ordem']


@admin.register(ProgressoUsuario)
class ProgressoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['atividade', 'usuario', 'concluida', 'data_conclusao', 'nota_auto_avaliacao']
    list_filter = ['concluida', 'nota_auto_avaliacao', 'created_at']
    search_fields = ['atividade__titulo', 'usuario__nome_completo']
    ordering = ['-created_at']
