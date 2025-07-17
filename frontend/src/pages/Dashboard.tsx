import React from 'react';

export const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Visão geral da sua jornada FIRE</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Gastos Este Mês</p>
              <p className="text-2xl font-bold text-gray-900">R$ 4.580</p>
              <p className="text-sm text-red-600">+5.2% vs mês anterior</p>
            </div>
            <div className="p-3 bg-red-100 rounded-full">
              <span className="text-2xl">💳</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Taxa de Poupança</p>
              <p className="text-2xl font-bold text-gray-900">42%</p>
              <p className="text-sm text-green-600">Excelente!</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <span className="text-2xl">💰</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Patrimônio Atual</p>
              <p className="text-2xl font-bold text-gray-900">R$ 580K</p>
              <p className="text-sm text-blue-600">32% da meta FIRE</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <span className="text-2xl">📈</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Anos para FIRE</p>
              <p className="text-2xl font-bold text-gray-900">8 anos</p>
              <p className="text-sm text-orange-600">Aos 38 anos</p>
            </div>
            <div className="p-3 bg-orange-100 rounded-full">
              <span className="text-2xl">🔥</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Expense Breakdown */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Gastos por Categoria</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-lg">🍽️</span>
                <span className="text-sm text-gray-700">Alimentação</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: '35%' }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900">R$ 1.200</span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-lg">🏠</span>
                <span className="text-sm text-gray-700">Moradia</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '30%' }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900">R$ 1.000</span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-lg">🚗</span>
                <span className="text-sm text-gray-700">Transporte</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '20%' }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900">R$ 600</span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-lg">🎬</span>
                <span className="text-sm text-gray-700">Lazer</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-purple-500 h-2 rounded-full" style={{ width: '15%' }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900">R$ 450</span>
              </div>
            </div>
          </div>
        </div>

        {/* FIRE Progress */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Progresso FIRE</h3>
          <div className="text-center">
            <div className="relative inline-flex items-center justify-center w-32 h-32 mb-4">
              <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  className="text-gray-200"
                />
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray="314"
                  strokeDashoffset="214"
                  className="text-orange-500"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl font-bold text-gray-900">32%</span>
              </div>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-gray-600">R$ 580.000 de R$ 1.800.000</p>
              <p className="text-xs text-gray-500">Faltam R$ 1.220.000 para FIRE</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Transactions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Transações Recentes</h3>
          <button className="text-sm text-blue-600 hover:text-blue-700">Ver todas</button>
        </div>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                <span className="text-sm">🍽️</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Supermercado Pão de Açúcar</p>
                <p className="text-xs text-gray-500">Hoje, 14:30</p>
              </div>
            </div>
            <span className="text-sm font-medium text-red-600">-R$ 180,50</span>
          </div>
          
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                <span className="text-sm">🚗</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Posto Shell</p>
                <p className="text-xs text-gray-500">Ontem, 18:45</p>
              </div>
            </div>
            <span className="text-sm font-medium text-red-600">-R$ 85,00</span>
          </div>
          
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <span className="text-sm">💰</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Salário</p>
                <p className="text-xs text-gray-500">25 Jan, 09:00</p>
              </div>
            </div>
            <span className="text-sm font-medium text-green-600">+R$ 8.000,00</span>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 transition-colors">
          <div className="flex items-center justify-center space-x-2">
            <span className="text-lg">📄</span>
            <span className="font-medium">Adicionar Gasto</span>
          </div>
        </button>
        
        <button className="bg-green-600 text-white p-4 rounded-lg hover:bg-green-700 transition-colors">
          <div className="flex items-center justify-center space-x-2">
            <span className="text-lg">📊</span>
            <span className="font-medium">Upload Extrato</span>
          </div>
        </button>
        
        <button className="bg-orange-600 text-white p-4 rounded-lg hover:bg-orange-700 transition-colors">
          <div className="flex items-center justify-center space-x-2">
            <span className="text-lg">🔥</span>
            <span className="font-medium">Calcular FIRE</span>
          </div>
        </button>
      </div>
    </div>
  );
};