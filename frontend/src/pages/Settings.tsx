import React from 'react';

export const Settings: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Configurações</h1>
        <p className="text-gray-600 mt-2">Personalize sua experiência FIRE Brasil</p>
      </div>

      {/* Profile Settings */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Perfil</h2>
        
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-gray-300 rounded-full flex items-center justify-center">
              <span className="text-xl font-bold text-gray-700">U</span>
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Usuário FIRE</h3>
              <p className="text-sm text-gray-600">usuario@email.com</p>
            </div>
            <button className="ml-auto bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Editar
            </button>
          </div>
        </div>
      </div>

      {/* FIRE Settings */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Configurações FIRE</h2>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Meta de Gastos Mensais</label>
            <input
              type="text"
              defaultValue="R$ 6.000,00"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-sm text-gray-600 mt-1">Valor que você pretende gastar na aposentadoria</p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Idade de Aposentadoria</label>
            <input
              type="number"
              defaultValue="40"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-sm text-gray-600 mt-1">Idade alvo para alcançar FIRE</p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Perfil de Investimento</label>
            <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option>Conservador (8% a.a.)</option>
              <option selected>Moderado (10% a.a.)</option>
              <option>Agressivo (12% a.a.)</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Taxa de Inflação (IPCA)</label>
            <input
              type="text"
              defaultValue="4.5%"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Expense Categories */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Categorias de Gastos</h2>
        
        <div className="space-y-3">
          {[
            { name: 'Alimentação', icon: '🍽️', enabled: true },
            { name: 'Moradia', icon: '🏠', enabled: true },
            { name: 'Transporte', icon: '🚗', enabled: true },
            { name: 'Saúde', icon: '💊', enabled: true },
            { name: 'Educação', icon: '📚', enabled: true },
            { name: 'Lazer', icon: '🎬', enabled: true },
            { name: 'Vestuário', icon: '👕', enabled: false },
            { name: 'Financeiro', icon: '💰', enabled: true },
            { name: 'Outros', icon: '📦', enabled: true }
          ].map((category, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <span className="text-lg">{category.icon}</span>
                <span className="text-sm font-medium text-gray-900">{category.name}</span>
              </div>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  defaultChecked={category.enabled}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
              </label>
            </div>
          ))}
        </div>
        
        <button className="mt-4 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
          + Adicionar Categoria
        </button>
      </div>

      {/* Notifications */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Notificações</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">Lembrete de Gastos</p>
              <p className="text-sm text-gray-600">Notificação quando gastos excedem orçamento</p>
            </div>
            <label className="flex items-center">
              <input
                type="checkbox"
                defaultChecked
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
            </label>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">Relatório Mensal</p>
              <p className="text-sm text-gray-600">Receber relatório automático por email</p>
            </div>
            <label className="flex items-center">
              <input
                type="checkbox"
                defaultChecked
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
            </label>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">Metas FIRE</p>
              <p className="text-sm text-gray-600">Atualizações sobre progresso FIRE</p>
            </div>
            <label className="flex items-center">
              <input
                type="checkbox"
                defaultChecked
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
            </label>
          </div>
        </div>
      </div>

      {/* Data & Privacy */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Dados e Privacidade</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">Backup Automático</p>
              <p className="text-sm text-gray-600">Fazer backup dos dados localmente</p>
            </div>
            <label className="flex items-center">
              <input
                type="checkbox"
                defaultChecked
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
            </label>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">Compartilhamento de Dados</p>
              <p className="text-sm text-gray-600">Permitir análise para melhorias</p>
            </div>
            <label className="flex items-center">
              <input
                type="checkbox"
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
            </label>
          </div>
          
          <div className="pt-4 border-t">
            <div className="flex space-x-4">
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Exportar Dados
              </button>
              <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
                Limpar Dados
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* About */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Sobre</h2>
        
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Versão</span>
            <span className="text-sm font-medium text-gray-900">1.0.0</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Última Atualização</span>
            <span className="text-sm font-medium text-gray-900">16 Jan 2024</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Desenvolvido por</span>
            <span className="text-sm font-medium text-gray-900">FIRE Brasil Team</span>
          </div>
        </div>
        
        <div className="mt-6 pt-4 border-t">
          <div className="flex space-x-4">
            <button className="text-blue-600 hover:text-blue-700 text-sm">
              Política de Privacidade
            </button>
            <button className="text-blue-600 hover:text-blue-700 text-sm">
              Termos de Uso
            </button>
            <button className="text-blue-600 hover:text-blue-700 text-sm">
              Suporte
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};