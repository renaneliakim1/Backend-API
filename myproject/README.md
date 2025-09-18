# API de Planos de Estudos - Documentação

## Visão Geral

Esta API REST foi desenvolvida em Django para gerenciar planos de estudos personalizados com integração de IA. O sistema permite que usuários se cadastrem, façam login e criem planos de estudo personalizados baseados em suas necessidades.

## Funcionalidades Principais

###  Autenticação
- Registro de usuários com campos customizados
- Login/logout com JWT
- Gestão de perfil de usuário
- Upload de foto de perfil

###  Gestão de Planos de Estudo
- Criação de planos de estudo personalizados
- Acompanhamento de progresso
- Gestão de atividades e disciplinas
- Estatísticas de desempenho

###  Integração com IA (Preparado)
- Endpoint preparado para geração de planos via IA
- Estrutura flexível para diferentes provedores de IA

## Endpoints da API

### Autenticação (`/api/v1/auth/`)

#### POST `/api/v1/auth/register/`
Registro de novo usuário
```json
{
  "email": "usuario@email.com",
  "username": "usuario",
  "nome_completo": "Nome Completo",
  "password": "senha123",
  "password_confirm": "senha123",
  "escolaridade": "superior",
  "disciplina_preferida": "matematica",
  "foto_perfil": "arquivo_imagem (opcional)"
}
```

#### POST `/api/v1/auth/login/`
Login de usuário
```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

#### GET/PUT `/api/v1/auth/profile/`
Visualizar/atualizar perfil do usuário

#### POST `/api/v1/auth/logout/`
Logout do usuário
```json
{
  "refresh_token": "token_refresh"
}
```

#### POST `/api/v1/auth/change-password/`
Alterar senha
```json
{
  "old_password": "senha_atual",
  "new_password": "nova_senha",
  "new_password_confirm": "nova_senha"
}
```

#### GET `/api/v1/auth/dashboard/`
Dados do dashboard do usuário

### Planos de Estudo (`/api/v1/study/`)

#### GET `/api/v1/study/disciplinas/`
Listar todas as disciplinas disponíveis

#### GET/POST `/api/v1/study/planos/`
Listar/criar planos de estudo do usuário

#### GET/PUT/DELETE `/api/v1/study/planos/{id}/`
Visualizar/atualizar/deletar plano específico

#### POST `/api/v1/study/planos/{id}/ativar/`
Ativar um plano de estudos

#### POST `/api/v1/study/planos/{id}/concluir/`
Marcar plano como concluído

#### GET `/api/v1/study/planos/{id}/atividades_semana/?semana=1`
Obter atividades de uma semana específica

#### GET `/api/v1/study/planos/{id}/estatisticas/`
Estatísticas detalhadas do plano

#### GET/POST `/api/v1/study/atividades/`
Listar/criar atividades

#### POST `/api/v1/study/atividades/{id}/marcar_concluida/`
Marcar atividade como concluída
```json
{
  "tempo_gasto_minutos": 45,
  "nota_auto_avaliacao": 4,
  "observacoes": "Exercício bem explicado"
}
```

#### GET/POST `/api/v1/study/progressos/`
Visualizar/registrar progresso

#### GET `/api/v1/study/dashboard/`
Estatísticas gerais do usuário

#### POST `/api/v1/study/gerar-plano-ia/`
Gerar plano usando IA (placeholder)
```json
{
  "objetivos": "Aprender matemática básica",
  "disciplinas_ids": [1, 2],
  "tempo_disponivel": "2 horas por dia",
  "nivel_dificuldade": "iniciante",
  "horas_por_semana": 10,
  "duracao_semanas": 8,
  "conhecimento_previo": "Básico em álgebra"
}
```

### JWT Tokens (`/api/v1/token/`)

#### POST `/api/v1/token/`
Obter tokens JWT
```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

#### POST `/api/v1/token/refresh/`
Renovar token de acesso
```json
{
  "refresh": "refresh_token"
}
```

#### POST `/api/v1/token/verify/`
Verificar validade do token
```json
{
  "token": "access_token"
}
```

## Modelos de Dados

### User (Usuário)
- email (único)
- username
- nome_completo
- escolaridade (choices)
- disciplina_preferida (choices)
- foto_perfil (ImageField)
- created_at, updated_at

### Disciplina
- nome
- descricao
- created_at

### PlanoEstudo
- usuario (ForeignKey)
- titulo
- descricao
- disciplinas (ManyToMany)
- nivel_dificuldade (choices)
- horas_por_semana
- duracao_semanas
- status (choices)
- datas (inicio, fim_prevista, fim_real)
- gerado_por_ia (boolean)
- prompt_usado (para IA)

### AtividadePlano
- plano (ForeignKey)
- disciplina (ForeignKey)
- titulo, descricao
- tipo (choices)
- semana, dia_semana, ordem
- tempo_estimado_minutos
- recursos_necessarios
- links_uteis (JSONField)

### ProgressoUsuario
- usuario (ForeignKey)
- atividade (ForeignKey)
- concluida (boolean)
- data_conclusao
- tempo_gasto_minutos
- nota_auto_avaliacao (1-5)
- observacoes

## Configurações

### CORS
Configurado para aceitar requests de:
- http://localhost:3000 (React)
- http://127.0.0.1:3000
- http://localhost:5173 (Vite)

### JWT
- Access Token: 60 minutos
- Refresh Token: 7 dias
- Tokens são rotacionados e adicionados à blacklist

### Upload de Arquivos
- Imagens de perfil: `media/profile_pictures/`
- Formatos aceitos: jpg, jpeg, png
- Servido em `/media/` durante desenvolvimento

## Como Executar

1. Ativar ambiente virtual:
```bash
.\venv\Scripts\Activate.ps1
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Executar migrações:
```bash
python manage.py migrate
```

4. Popular disciplinas:
```bash
python manage.py populate_disciplines
```

5. Criar superusuário:
```bash
python manage.py createsuperuser
```

6. Executar servidor:
```bash
python manage.py runserver
```

## Admin Interface

Acesse `/admin/` para gerenciar:
- Usuários
- Disciplinas
- Planos de Estudo
- Atividades
- Progressos

## Próximos Passos

1. **Integração com IA**: Implementar serviços de IA (OpenAI, Anthropic, etc.)
2. **Notificações**: Sistema de lembretes e notificações
3. **Gamificação**: Pontos, badges, conquistas
4. **Relatórios**: Relatórios detalhados de progresso
5. **Social**: Compartilhamento de planos e progresso
6. **Mobile**: Aplicativo móvel React Native

## Estrutura do Projeto

```
myproject/
├── accounts/           # App de usuários
├── study_plans/        # App de planos de estudo
├── myproject/          # Configurações do projeto
├── media/              # Arquivos de upload
├── static/             # Arquivos estáticos
├── requirements.txt    # Dependências
├── .env               # Variáveis de ambiente
└── .gitignore         # Exclusões do Git
```

Este backend está pronto para integração com frontend.