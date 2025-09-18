"""
Script para popular o banco de dados com disciplinas básicas
Execute com: python manage.py shell < populate_data.py
"""

from study_plans.models import Disciplina

# Lista de disciplinas básicas
disciplinas = [
    {'nome': 'Matemática', 'descricao': 'Álgebra, geometria, cálculo e estatística'},
    {'nome': 'Português', 'descricao': 'Gramática, literatura e redação'},
    {'nome': 'História', 'descricao': 'História geral e do Brasil'},
    {'nome': 'Geografia', 'descricao': 'Geografia física e humana'},
    {'nome': 'Física', 'descricao': 'Mecânica, termodinâmica, óptica e eletromagnetismo'},
    {'nome': 'Química', 'descricao': 'Química geral, orgânica e inorgânica'},
    {'nome': 'Biologia', 'descricao': 'Citologia, genética, ecologia e evolução'},
    {'nome': 'Inglês', 'descricao': 'Gramática, vocabulário e conversação'},
    {'nome': 'Espanhol', 'descricao': 'Gramática, vocabulário e conversação'},
    {'nome': 'Filosofia', 'descricao': 'História da filosofia e pensamento crítico'},
    {'nome': 'Sociologia', 'descricao': 'Sociedade, cultura e instituições sociais'},
    {'nome': 'Artes', 'descricao': 'História da arte, técnicas artísticas'},
    {'nome': 'Educação Física', 'descricao': 'Esportes, saúde e bem-estar'},
    {'nome': 'Informática', 'descricao': 'Programação, banco de dados e redes'},
    {'nome': 'Economia', 'descricao': 'Microeconomia, macroeconomia e finanças'},
    {'nome': 'Psicologia', 'descricao': 'Comportamento humano e processos mentais'},
]

# Criar disciplinas
for disciplina_data in disciplinas:
    disciplina, created = Disciplina.objects.get_or_create(
        nome=disciplina_data['nome'],
        defaults={'descricao': disciplina_data['descricao']}
    )
    if created:
        print(f"Disciplina '{disciplina.nome}' criada com sucesso!")
    else:
        print(f"Disciplina '{disciplina.nome}' já existe.")

print(f"\nTotal de disciplinas no banco: {Disciplina.objects.count()}")