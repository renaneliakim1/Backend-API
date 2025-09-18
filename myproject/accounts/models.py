from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    """
    Modelo de usuário customizado para a aplicação de planos de estudo
    """
    ESCOLARIDADE_CHOICES = [
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('superior', 'Ensino Superior'),
        ('pos_graduacao', 'Pós-graduação'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    ]
    
    DISCIPLINA_CHOICES = [
        ('matematica', 'Matemática'),
        ('portugues', 'Português'),
        ('historia', 'História'),
        ('geografia', 'Geografia'),
        ('ciencias', 'Ciências'),
        ('fisica', 'Física'),
        ('quimica', 'Química'),
        ('biologia', 'Biologia'),
        ('ingles', 'Inglês'),
        ('espanhol', 'Espanhol'),
        ('filosofia', 'Filosofia'),
        ('sociologia', 'Sociologia'),
        ('artes', 'Artes'),
        ('educacao_fisica', 'Educação Física'),
        ('informatica', 'Informática'),
        ('outro', 'Outro'),
    ]
    
    # Sobrescrever o campo email para ser único e obrigatório
    email = models.EmailField(unique=True)
    
    # Campos adicionais
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    escolaridade = models.CharField(
        max_length=20,
        choices=ESCOLARIDADE_CHOICES,
        verbose_name="Escolaridade"
    )
    disciplina_preferida = models.CharField(
        max_length=20,
        choices=DISCIPLINA_CHOICES,
        verbose_name="Disciplina Preferida"
    )
    foto_perfil = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Foto de Perfil"
    )
    
    # Campos de controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Configurar email como campo de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome_completo']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
    def __str__(self):
        return f"{self.nome_completo} ({self.email})"
    
    def get_full_name(self):
        return self.nome_completo
    
    def get_short_name(self):
        return self.nome_completo.split()[0] if self.nome_completo else self.username
