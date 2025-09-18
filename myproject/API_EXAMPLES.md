# Exemplos de Requests para Testar a API

## Configuração Base
```
Base URL: http://127.0.0.1:8000/api/v1
Content-Type: application/json
```

## 1. Registro de Usuário
```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "email": "teste@email.com",
  "username": "teste_usuario",
  "nome_completo": "Usuário de Teste",
  "password": "senha123456",
  "password_confirm": "senha123456",
  "escolaridade": "superior",
  "disciplina_preferida": "matematica"
}
```

## 2. Login
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "teste@email.com",
  "password": "senha123456"
}
```

Resposta:
```json
{
  "message": "Login realizado com sucesso!",
  "user": {
    "id": 1,
    "email": "teste@email.com",
    "nome_completo": "Usuário de Teste",
    "escolaridade": "superior",
    "disciplina_preferida": "matematica"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

## 3. Listar Disciplinas
```http
GET /api/v1/study/disciplinas/
Authorization: Bearer {access_token}
```

## 4. Buscar Perfil do Usuário
```http
GET /api/v1/auth/profile/
Authorization: Bearer {access_token}
```

## 5. Atualizar Perfil
```http
PUT /api/v1/auth/profile/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome_completo": "Novo Nome Completo",
  "escolaridade": "pos_graduacao",
  "disciplina_preferida": "fisica"
}
```

## 6. Criar Plano de Estudo
```http
POST /api/v1/study/planos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "titulo": "Plano de Matemática Básica",
  "descricao": "Estudar fundamentos de matemática",
  "disciplinas_ids": [1],
  "nivel_dificuldade": "iniciante",
  "horas_por_semana": 10,
  "duracao_semanas": 8
}
```

## 7. Listar Planos do Usuário
```http
GET /api/v1/study/planos/
Authorization: Bearer {access_token}
```

## 8. Gerar Plano com IA (Placeholder)
```http
POST /api/v1/study/gerar-plano-ia/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "objetivos": "Aprender matemática para vestibular",
  "disciplinas_ids": [1],
  "tempo_disponivel": "2 horas por dia",
  "nivel_dificuldade": "intermediario",
  "horas_por_semana": 14,
  "duracao_semanas": 12,
  "conhecimento_previo": "Ensino médio completo"
}
```

## 9. Ativar Plano
```http
POST /api/v1/study/planos/{id}/ativar/
Authorization: Bearer {access_token}
```

## 10. Marcar Atividade como Concluída
```http
POST /api/v1/study/atividades/{id}/marcar_concluida/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "tempo_gasto_minutos": 45,
  "nota_auto_avaliacao": 4,
  "observacoes": "Exercício bem explicado, entendi os conceitos"
}
```

## 11. Dashboard do Usuário (Autenticação)
```http
GET /api/v1/auth/dashboard/
Authorization: Bearer {access_token}
```

## 12. Dashboard de Estudos
```http
GET /api/v1/study/dashboard/
Authorization: Bearer {access_token}
```

## 13. Estatísticas de um Plano
```http
GET /api/v1/study/planos/{id}/estatisticas/
Authorization: Bearer {access_token}
```

## 14. Atividades de uma Semana
```http
GET /api/v1/study/planos/{id}/atividades_semana/?semana=1
Authorization: Bearer {access_token}
```

## 15. Alterar Senha
```http
POST /api/v1/auth/change-password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "senha123456",
  "new_password": "nova_senha123",
  "new_password_confirm": "nova_senha123"
}
```

## 16. Logout
```http
POST /api/v1/auth/logout/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "refresh_token": "{refresh_token}"
}
```

## 17. Renovar Token
```http
POST /api/v1/token/refresh/
Content-Type: application/json

{
  "refresh": "{refresh_token}"
}
```

## Upload de Foto de Perfil
```http
PATCH /api/v1/auth/profile/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

Form Data:
foto_perfil: [arquivo_imagem.jpg]
```

## Códigos de Status HTTP

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Erro de validação/dados inválidos
- `401` - Não autenticado
- `403` - Sem permissão
- `404` - Não encontrado
- `500` - Erro interno do servidor

## Estrutura de Erro Padrão
```json
{
  "error": "Mensagem de erro",
  "details": {
    "campo": ["Lista de erros do campo"]
  }
}
```

## Headers Importantes

### Para requests autenticados:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

### Para upload de arquivos:
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

## Teste Rápido com cURL

### Registrar usuário:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "username": "teste_usuario",
    "nome_completo": "Usuário de Teste",
    "password": "senha123456",
    "password_confirm": "senha123456",
    "escolaridade": "superior",
    "disciplina_preferida": "matematica"
  }'
```

### Login:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "password": "senha123456"
  }'
```