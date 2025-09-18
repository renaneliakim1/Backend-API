from rest_framework import serializers
from .models import Disciplina, PlanoEstudo, AtividadePlano, ProgressoUsuario
from accounts.serializers import UserSerializer


class DisciplinaSerializer(serializers.ModelSerializer):
    """
    Serializer para disciplinas
    """
    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'descricao', 'created_at']


class AtividadePlanoSerializer(serializers.ModelSerializer):
    """
    Serializer para atividades do plano
    """
    disciplina = DisciplinaSerializer(read_only=True)
    disciplina_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AtividadePlano
        fields = [
            'id', 'titulo', 'descricao', 'tipo', 'semana', 'dia_semana',
            'ordem', 'tempo_estimado_minutos', 'recursos_necessarios',
            'links_uteis', 'disciplina', 'disciplina_id', 'created_at'
        ]


class PlanoEstudoSerializer(serializers.ModelSerializer):
    """
    Serializer para planos de estudo
    """
    disciplinas = DisciplinaSerializer(many=True, read_only=True)
    disciplinas_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    atividades = AtividadePlanoSerializer(many=True, read_only=True)
    usuario = UserSerializer(read_only=True)
    total_atividades = serializers.SerializerMethodField()
    atividades_concluidas = serializers.SerializerMethodField()
    progresso_percentual = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanoEstudo
        fields = [
            'id', 'titulo', 'descricao', 'disciplinas', 'disciplinas_ids',
            'nivel_dificuldade', 'horas_por_semana', 'duracao_semanas',
            'status', 'data_inicio', 'data_fim_prevista', 'data_fim_real',
            'gerado_por_ia', 'prompt_usado', 'usuario', 'atividades',
            'total_atividades', 'atividades_concluidas', 'progresso_percentual',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['usuario', 'created_at', 'updated_at']
    
    def get_total_atividades(self, obj):
        return obj.atividades.count()
    
    def get_atividades_concluidas(self, obj):
        user = self.context['request'].user if 'request' in self.context else None
        if user:
            return obj.atividades.filter(
                progressos__usuario=user,
                progressos__concluida=True
            ).count()
        return 0
    
    def get_progresso_percentual(self, obj):
        total = self.get_total_atividades(obj)
        concluidas = self.get_atividades_concluidas(obj)
        return round((concluidas / total * 100) if total > 0 else 0, 2)
    
    def create(self, validated_data):
        disciplinas_ids = validated_data.pop('disciplinas_ids', [])
        validated_data['usuario'] = self.context['request'].user
        plano = super().create(validated_data)
        
        if disciplinas_ids:
            plano.disciplinas.set(disciplinas_ids)
        
        return plano
    
    def update(self, instance, validated_data):
        disciplinas_ids = validated_data.pop('disciplinas_ids', None)
        plano = super().update(instance, validated_data)
        
        if disciplinas_ids is not None:
            plano.disciplinas.set(disciplinas_ids)
        
        return plano


class PlanoEstudoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para criação de planos via IA
    """
    disciplinas_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    objetivos = serializers.CharField(write_only=True, help_text="Objetivos do usuário")
    tempo_disponivel = serializers.CharField(write_only=True, help_text="Tempo disponível para estudos")
    conhecimento_previo = serializers.CharField(write_only=True, required=False, help_text="Conhecimento prévio do usuário")
    
    class Meta:
        model = PlanoEstudo
        fields = [
            'titulo', 'disciplinas_ids', 'nivel_dificuldade', 'horas_por_semana',
            'duracao_semanas', 'objetivos', 'tempo_disponivel', 'conhecimento_previo'
        ]
    
    def create(self, validated_data):
        # Extrair dados para IA
        disciplinas_ids = validated_data.pop('disciplinas_ids')
        objetivos = validated_data.pop('objetivos')
        tempo_disponivel = validated_data.pop('tempo_disponivel')
        conhecimento_previo = validated_data.pop('conhecimento_previo', '')
        
        # Criar prompt para IA
        prompt = f"""
        Objetivos: {objetivos}
        Tempo disponível: {tempo_disponivel}
        Conhecimento prévio: {conhecimento_previo}
        Nível: {validated_data.get('nivel_dificuldade')}
        Horas por semana: {validated_data.get('horas_por_semana')}
        Duração: {validated_data.get('duracao_semanas')} semanas
        """
        
        validated_data['prompt_usado'] = prompt
        validated_data['usuario'] = self.context['request'].user
        validated_data['gerado_por_ia'] = True
        
        plano = super().create(validated_data)
        plano.disciplinas.set(disciplinas_ids)
        
        return plano


class ProgressoUsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para progresso do usuário
    """
    atividade = AtividadePlanoSerializer(read_only=True)
    atividade_id = serializers.IntegerField(write_only=True)
    usuario = UserSerializer(read_only=True)
    
    class Meta:
        model = ProgressoUsuario
        fields = [
            'id', 'atividade', 'atividade_id', 'usuario', 'concluida',
            'data_conclusao', 'tempo_gasto_minutos', 'nota_auto_avaliacao',
            'observacoes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['usuario', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class PlanoEstudoResumoSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem de planos
    """
    disciplinas_count = serializers.SerializerMethodField()
    progresso_percentual = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanoEstudo
        fields = [
            'id', 'titulo', 'status', 'nivel_dificuldade',
            'horas_por_semana', 'duracao_semanas', 'disciplinas_count',
            'progresso_percentual', 'created_at'
        ]
    
    def get_disciplinas_count(self, obj):
        return obj.disciplinas.count()
    
    def get_progresso_percentual(self, obj):
        user = self.context['request'].user if 'request' in self.context else None
        if user:
            total = obj.atividades.count()
            concluidas = obj.atividades.filter(
                progressos__usuario=user,
                progressos__concluida=True
            ).count()
            return round((concluidas / total * 100) if total > 0 else 0, 2)
        return 0