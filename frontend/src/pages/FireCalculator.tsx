import React, { useState } from 'react';

export const FireCalculator: React.FC = () => {
  const [formData, setFormData] = useState({
    currentAge: '',
    monthlyIncome: '',
    monthlyExpenses: '',
    currentSavings: '',
    investmentProfile: 'moderado',
    fireScenario: 'regular_fire'
  });

  const [results, setResults] = useState<any>(null);

  const handleCalculate = () => {
    // Simulação de cálculo
    const mockResults = {
      fireNumber: 1800000,
      yearsToFire: 8,
      targetAge: 38,
      monthlySavingsNeeded: 3200,
      savingsRate: 40,
      scenarios: {
        lean_fire: { fireNumber: 900000, years: 5 },
        regular_fire: { fireNumber: 1800000, years: 8 },
        fat_fire: { fireNumber: 4500000, years: 15 }
      }
    };
    setResults(mockResults);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Calculadora FIRE</h1>
        <p className="text-gray-600 mt-2">Calcule seu caminho para a independência financeira</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Seus Dados</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Idade Atual</label>
              <input
                type="number"
                value={formData.currentAge}
                onChange={(e) => setFormData({...formData, currentAge: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="30"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Renda Mensal Líquida</label>
              <input
                type="text"
                value={formData.monthlyIncome}
                onChange={(e) => setFormData({...formData, monthlyIncome: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="R$ 8.000,00"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Gastos Mensais</label>
              <input
                type="text"
                value={formData.monthlyExpenses}
                onChange={(e) => setFormData({...formData, monthlyExpenses: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="R$ 4.800,00"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Patrimônio Atual</label>
              <input
                type="text"
                value={formData.currentSavings}
                onChange={(e) => setFormData({...formData, currentSavings: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="R$ 50.000,00"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Perfil de Investimento</label>
              <select
                value={formData.investmentProfile}
                onChange={(e) => setFormData({...formData, investmentProfile: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="conservador">Conservador (8% a.a.)</option>
                <option value="moderado">Moderado (10% a.a.)</option>
                <option value="agressivo">Agressivo (12% a.a.)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Cenário FIRE</label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="fireScenario"
                    value="lean_fire"
                    checked={formData.fireScenario === 'lean_fire'}
                    onChange={(e) => setFormData({...formData, fireScenario: e.target.value})}
                    className="mr-2"
                  />
                  <span className="text-sm">Lean FIRE - R$ 3.000/mês</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="fireScenario"
                    value="regular_fire"
                    checked={formData.fireScenario === 'regular_fire'}
                    onChange={(e) => setFormData({...formData, fireScenario: e.target.value})}
                    className="mr-2"
                  />
                  <span className="text-sm">Regular FIRE - R$ 6.000/mês</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="fireScenario"
                    value="fat_fire"
                    checked={formData.fireScenario === 'fat_fire'}
                    onChange={(e) => setFormData({...formData, fireScenario: e.target.value})}
                    className="mr-2"
                  />
                  <span className="text-sm">Fat FIRE - R$ 15.000/mês</span>
                </label>
              </div>
            </div>

            <button
              onClick={handleCalculate}
              className="w-full bg-orange-600 text-white py-3 rounded-lg hover:bg-orange-700 transition-colors font-medium"
            >
              🔥 Calcular FIRE
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-6">
          {results ? (
            <>
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Seus Resultados FIRE</h2>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-orange-50 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600">
                      {results.yearsToFire} anos
                    </div>
                    <div className="text-sm text-gray-600">Para FIRE</div>
                  </div>
                  
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">
                      {results.targetAge} anos
                    </div>
                    <div className="text-sm text-gray-600">Idade FIRE</div>
                  </div>
                  
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">
                      R$ {results.monthlySavingsNeeded.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Poupança/mês</div>
                  </div>
                  
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">
                      {results.savingsRate}%
                    </div>
                    <div className="text-sm text-gray-600">Taxa poupança</div>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Comparação de Cenários</h3>
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <span className="font-medium text-gray-900">Lean FIRE</span>
                      <span className="text-sm text-gray-600 ml-2">R$ 3.000/mês</span>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-gray-900">{results.scenarios.lean_fire.years} anos</div>
                      <div className="text-sm text-gray-600">R$ {results.scenarios.lean_fire.fireNumber.toLocaleString()}</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <div>
                      <span className="font-medium text-blue-900">Regular FIRE</span>
                      <span className="text-sm text-blue-700 ml-2">R$ 6.000/mês</span>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-blue-900">{results.scenarios.regular_fire.years} anos</div>
                      <div className="text-sm text-blue-700">R$ {results.scenarios.regular_fire.fireNumber.toLocaleString()}</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <span className="font-medium text-gray-900">Fat FIRE</span>
                      <span className="text-sm text-gray-600 ml-2">R$ 15.000/mês</span>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-gray-900">{results.scenarios.fat_fire.years} anos</div>
                      <div className="text-sm text-gray-600">R$ {results.scenarios.fat_fire.fireNumber.toLocaleString()}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Insights e Recomendações</h3>
                
                <div className="space-y-3">
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                    <p className="text-sm text-gray-700">
                      Com uma taxa de poupança de 40%, você está no caminho certo para FIRE!
                    </p>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <p className="text-sm text-gray-700">
                      Considere diversificar entre Tesouro Direto, ações e FIIs para otimizar retornos.
                    </p>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-orange-500 rounded-full mt-2"></div>
                    <p className="text-sm text-gray-700">
                      Revisar gastos mensais pode acelerar sua jornada FIRE em 2-3 anos.
                    </p>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🔥</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Calcule seu FIRE</h3>
                <p className="text-gray-600">Preencha os dados ao lado para descobrir seu caminho para a independência financeira.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};