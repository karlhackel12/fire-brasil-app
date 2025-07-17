import React from 'react';

export const Reports: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Relatórios</h1>
        <p className="text-gray-600 mt-2">Análises detalhadas dos seus gastos e progresso FIRE</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Relatório Mensal</h3>
          <p className="text-3xl font-bold text-blue-600 mb-2">Janeiro 2024</p>
          <p className="text-sm text-gray-600">Análise completa do mês</p>
          <button className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Ver Relatório
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Progresso FIRE</h3>
          <p className="text-3xl font-bold text-orange-600 mb-2">32%</p>
          <p className="text-sm text-gray-600">R$ 580K de R$ 1.8M</p>
          <button className="mt-4 w-full bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition-colors">
            Ver Detalhes
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Análise Anual</h3>
          <p className="text-3xl font-bold text-green-600 mb-2">2024</p>
          <p className="text-sm text-gray-600">Tendências e insights</p>
          <button className="mt-4 w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors">
            Ver Análise
          </button>
        </div>
      </div>

      {/* Detailed Report */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Relatório Detalhado - Janeiro 2024</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Expense Analysis */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Análise de Gastos</h3>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Total de Gastos</span>
                <span className="text-2xl font-bold text-red-600">R$ 4.580,00</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Variação vs Mês Anterior</span>
                <span className="text-red-600">+5.2%</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Maior Categoria</span>
                <span className="text-gray-900">Alimentação (R$ 1.200)</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Média por Transação</span>
                <span className="text-gray-900">R$ 76,33</span>
              </div>
            </div>
          </div>
          
          {/* Savings Analysis */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Análise de Poupança</h3>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Poupança do Mês</span>
                <span className="text-2xl font-bold text-green-600">R$ 3.420,00</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Taxa de Poupança</span>
                <span className="text-green-600">42.8%</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Meta Mensal</span>
                <span className="text-gray-900">R$ 3.200,00</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Performance</span>
                <span className="text-green-600">+6.9% acima da meta</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Category Trends */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Tendências por Categoria</h2>
        
        <div className="space-y-4">
          {[
            { category: 'Alimentação', current: 1200, previous: 1100, change: '+9.1%', color: 'red' },
            { category: 'Transporte', current: 800, previous: 850, change: '-5.9%', color: 'green' },
            { category: 'Moradia', current: 1000, previous: 1000, change: '0%', color: 'gray' },
            { category: 'Lazer', current: 450, previous: 380, change: '+18.4%', color: 'red' },
            { category: 'Saúde', current: 380, previous: 320, change: '+18.8%', color: 'red' },
          ].map((item, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-medium">{item.category.charAt(0)}</span>
                </div>
                <div>
                  <div className="font-medium text-gray-900">{item.category}</div>
                  <div className="text-sm text-gray-600">R$ {item.current.toLocaleString()}</div>
                </div>
              </div>
              <div className="text-right">
                <div className={`text-sm font-medium ${
                  item.color === 'red' ? 'text-red-600' : 
                  item.color === 'green' ? 'text-green-600' : 'text-gray-600'
                }`}>
                  {item.change}
                </div>
                <div className="text-xs text-gray-500">vs mês anterior</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Insights */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Insights e Recomendações</h2>
        
        <div className="space-y-4">
          <div className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
            <div>
              <p className="text-sm font-medium text-blue-900">Economia Identificada</p>
              <p className="text-sm text-blue-700">
                Você gastou R$ 450 em lazer este mês, 18% acima do normal. 
                Considere reduzir para R$ 350 para acelerar seu FIRE.
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-3 p-4 bg-green-50 rounded-lg">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
            <div>
              <p className="text-sm font-medium text-green-900">Parabéns!</p>
              <p className="text-sm text-green-700">
                Sua taxa de poupança de 42.8% está excelente! 
                Você está 6.9% acima da sua meta mensal.
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-3 p-4 bg-yellow-50 rounded-lg">
            <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
            <div>
              <p className="text-sm font-medium text-yellow-900">Atenção</p>
              <p className="text-sm text-yellow-700">
                Gastos com alimentação aumentaram 9.1%. 
                Considere meal prep ou cozinhar mais em casa.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};