import axios from 'axios';

// Configuração da API
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para requests
api.interceptors.request.use(
  (config) => {
    // Adicionar autenticação quando implementada
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Redirect para login quando implementado
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Tipos
export interface ExpenseData {
  date: string;
  description: string;
  amount: number;
  category?: string;
  subcategory?: string;
  payment_method?: string;
  notes?: string;
}

export interface FireCalculationRequest {
  current_age: number;
  monthly_income: number;
  monthly_expenses: number;
  current_savings: number;
  investment_profile: string;
  fire_scenario: string;
}

// Funções da API
export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },

  // Expenses
  async addExpense(expense: ExpenseData) {
    const formData = new FormData();
    Object.entries(expense).forEach(([key, value]) => {
      formData.append(key, value.toString());
    });
    
    const response = await api.post('/expenses/manual', formData);
    return response.data;
  },

  async uploadDocument(file: File, userId: string = 'default') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);
    
    const response = await api.post('/upload/document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // FIRE Calculator
  async calculateFire(data: FireCalculationRequest, userId: string = 'default') {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value.toString());
    });
    formData.append('user_id', userId);
    
    const response = await api.post('/fire/calculate', formData);
    return response.data;
  },

  async getFireScenarios(userId: string = 'default') {
    const response = await api.get(`/fire/scenarios/${userId}`);
    return response.data;
  },

  // Dashboard
  async getDashboard(userId: string = 'default') {
    const response = await api.get(`/analysis/dashboard/${userId}`);
    return response.data;
  },

  async getInsights(userId: string = 'default') {
    const response = await api.get(`/analysis/insights/${userId}`);
    return response.data;
  },

  async getMonthlyReport(userId: string = 'default', month?: string) {
    const params = month ? `?month=${month}` : '';
    const response = await api.get(`/analysis/monthly-report/${userId}${params}`);
    return response.data;
  },

  // Configuration
  async getCategories() {
    const response = await api.get('/config/categories');
    return response.data;
  },

  async getInvestmentTypes() {
    const response = await api.get('/config/investment-types');
    return response.data;
  },
};

export default api;