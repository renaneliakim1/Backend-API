/**
 * Configuração da API para o frontend React
 * 
 * Este arquivo contém todas as configurações necessárias para
 * conectar o frontend React com o backend Django.
 */

// URL base da API
export const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Endpoints da API
export const API_ENDPOINTS = {
  // Autenticação
  auth: {
    register: '/auth/register/',
    login: '/auth/login/',
    logout: '/auth/logout/',
    profile: '/auth/profile/',
    changePassword: '/auth/change-password/',
    dashboard: '/auth/dashboard/',
  },
  
  // JWT Tokens
  token: {
    obtain: '/token/',
    refresh: '/token/refresh/',
    verify: '/token/verify/',
  },
  
  // Planos de Estudo
  study: {
    disciplinas: '/study/disciplinas/',
    planos: '/study/planos/',
    atividades: '/study/atividades/',
    progressos: '/study/progressos/',
    dashboard: '/study/dashboard/',
    gerarPlanoIA: '/study/gerar-plano-ia/',
  }
};

// Configuração do Axios (exemplo)
export const axiosConfig = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// Helper para URLs completas
export const getApiUrl = (endpoint) => `${API_BASE_URL}${endpoint}`;

// Exemplo de uso no React:
/*
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS, axiosConfig } from './config/api';

// Configurar axios
const api = axios.create(axiosConfig);

// Interceptor para adicionar token JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Exemplos de uso:

// 1. Registro de usuário
const register = async (userData) => {
  try {
    const response = await api.post(API_ENDPOINTS.auth.register, userData);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// 2. Login
const login = async (email, password) => {
  try {
    const response = await api.post(API_ENDPOINTS.auth.login, {
      email,
      password
    });
    
    // Salvar tokens
    localStorage.setItem('access_token', response.data.tokens.access);
    localStorage.setItem('refresh_token', response.data.tokens.refresh);
    
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// 3. Buscar disciplinas
const getDisciplinas = async () => {
  try {
    const response = await api.get(API_ENDPOINTS.study.disciplinas);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// 4. Criar plano de estudo
const createPlano = async (planoData) => {
  try {
    const response = await api.post(API_ENDPOINTS.study.planos, planoData);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// 5. Upload de foto de perfil
const uploadFotoPerfil = async (file) => {
  const formData = new FormData();
  formData.append('foto_perfil', file);
  
  try {
    const response = await api.patch(API_ENDPOINTS.auth.profile, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};
*/