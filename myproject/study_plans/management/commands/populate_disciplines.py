from django.core.management.base import BaseCommand
from study_plans.models import Disciplina


class Command(BaseCommand):
    help = 'Popula o banco de dados com disciplinas basicas'
    
    def handle(self, *args, **options):
        disciplinas = [
            {'nome': 'Matematica', 'descricao': 'Algebra, geometria, calculo e estatistica'},
            {'nome': 'Portugues', 'descricao': 'Gramatica, literatura e redacao'},
            {'nome': 'Historia', 'descricao': 'Historia geral e do Brasil'},
            {'nome': 'Geografia', 'descricao': 'Geografia fisica e humana'},
            {'nome': 'Fisica', 'descricao': 'Mecanica, termodinamica, optica e eletromagnetismo'},
            {'nome': 'Quimica', 'descricao': 'Quimica geral, organica e inorganica'},
            {'nome': 'Biologia', 'descricao': 'Citologia, genetica, ecologia e evolucao'},
            {'nome': 'Ingles', 'descricao': 'Gramatica, vocabulario e conversacao'},
            {'nome': 'Espanhol', 'descricao': 'Gramatica, vocabulario e conversacao'},
            {'nome': 'Filosofia', 'descricao': 'Historia da filosofia e pensamento critico'},
            {'nome': 'Sociologia', 'descricao': 'Sociedade, cultura e instituicoes sociais'},
            {'nome': 'Artes', 'descricao': 'Historia da arte, tecnicas artisticas'},
            {'nome': 'Educacao Fisica', 'descricao': 'Esportes, saude e bem-estar'},
            {'nome': 'Informatica', 'descricao': 'Programacao, banco de dados e redes'},
            {'nome': 'Economia', 'descricao': 'Microeconomia, macroeconomia e financas'},
            {'nome': 'Psicologia', 'descricao': 'Comportamento humano e processos mentais'},
        ]
        
        created_count = 0
        for disciplina_data in disciplinas:
            disciplina, created = Disciplina.objects.get_or_create(
                nome=disciplina_data['nome'],
                defaults={'descricao': disciplina_data['descricao']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Disciplina '{disciplina.nome}' criada com sucesso!")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Disciplina '{disciplina.nome}' ja existe.")
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nComando executado com sucesso! "
                f"{created_count} disciplinas criadas. "
                f"Total no banco: {Disciplina.objects.count()}"
            )
        )