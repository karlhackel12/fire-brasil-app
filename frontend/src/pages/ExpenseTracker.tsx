import React, { useState } from 'react';

export const ExpenseTracker: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'upload' | 'manual' | 'list'>('upload');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Controle de Gastos</h1>
        <p className="text-gray-600 mt-2">Gerencie suas despesas e categorize automaticamente</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('upload')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'upload'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📄 Upload de Documentos
            </button>
            <button
              onClick={() => setActiveTab('manual')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'manual'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              ✏️ Entrada Manual
            </button>
            <button
              onClick={() => setActiveTab('list')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'list'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📋 Lista de Gastos
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'upload' && <UploadTab />}
          {activeTab === 'manual' && <ManualEntryTab />}
          {activeTab === 'list' && <ExpenseListTab />}
        </div>
      </div>
    </div>
  );
};

const UploadTab: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-12">
          <div className="mx-auto w-12 h-12 mb-4 text-gray-400">
            <svg fill="none" stroke="currentColor" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <p className="text-lg font-medium text-gray-900 mb-2">Arraste arquivos aqui ou clique para selecionar</p>
          <p className="text-sm text-gray-600 mb-4">Suporte para PDF, Excel, CSV e imagens</p>
          <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Selecionar Arquivos
          </button>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="text-sm font-medium text-gray-900 mb-3">Formatos Suportados:</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="flex items-center space-x-2">
            <span className="text-red-500">📄</span>
            <span className="text-sm text-gray-600">PDF</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-green-500">📊</span>
            <span className="text-sm text-gray-600">Excel</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-blue-500">📋</span>
            <span className="text-sm text-gray-600">CSV</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-purple-500">🖼️</span>
            <span className="text-sm text-gray-600">Imagens</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const ManualEntryTab: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Data</label>
          <input
            type="date"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Valor</label>
          <input
            type="text"
            placeholder="R$ 0,00"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
        <input
          type="text"
          placeholder="Ex: Supermercado Pão de Açúcar"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Categoria</label>
          <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Selecione uma categoria</option>
            <option>🍽️ Alimentação</option>
            <option>🏠 Moradia</option>
            <option>🚗 Transporte</option>
            <option>💊 Saúde</option>
            <option>🎬 Lazer</option>
            <option>👕 Vestuário</option>
            <option>💰 Financeiro</option>
            <option>📦 Outros</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Método de Pagamento</label>
          <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Selecione um método</option>
            <option>💳 Cartão de Débito</option>
            <option>💳 Cartão de Crédito</option>
            <option>💰 Dinheiro</option>
            <option>📱 PIX</option>
            <option>📄 Boleto</option>
            <option>🏦 Transferência</option>
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Notas (opcional)</label>
        <textarea
          rows={3}
          placeholder="Adicione observações sobre esta despesa..."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="flex justify-end space-x-4">
        <button className="px-6 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          Adicionar Gasto
        </button>
      </div>
    </div>
  );
};

const ExpenseListTab: React.FC = () => {
  const expenses = [
    { id: 1, date: '2024-01-16', description: 'Supermercado Pão de Açúcar', category: 'Alimentação', amount: 250.00, method: 'Débito' },
    { id: 2, date: '2024-01-15', description: 'Posto Shell', category: 'Transporte', amount: 80.00, method: 'Crédito' },
    { id: 3, date: '2024-01-14', description: 'Farmácia Droga Raia', category: 'Saúde', amount: 45.00, method: 'PIX' },
    { id: 4, date: '2024-01-13', description: 'Cinema Cinemark', category: 'Lazer', amount: 60.00, method: 'Débito' },
    { id: 5, date: '2024-01-12', description: 'Uber', category: 'Transporte', amount: 25.00, method: 'Crédito' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Gastos Recentes</h3>
          <p className="text-sm text-gray-600">Últimas transações adicionadas</p>
        </div>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
          Exportar
        </button>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Método</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Valor</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {expenses.map((expense) => (
              <tr key={expense.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {new Date(expense.date).toLocaleDateString('pt-BR')}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {expense.description}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {expense.category}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {expense.method}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-red-600">
                  -R$ {expense.amount.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button className="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                  <button className="text-red-600 hover:text-red-900">Excluir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};