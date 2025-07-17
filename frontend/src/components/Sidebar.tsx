import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const navigation = [
  { name: 'Dashboard', href: '/', icon: '📊' },
  { name: 'Controle de Gastos', href: '/expenses', icon: '💳' },
  { name: 'Calculadora FIRE', href: '/fire-calculator', icon: '🔥' },
  { name: 'Relatórios', href: '/reports', icon: '📈' },
  { name: 'Configurações', href: '/settings', icon: '⚙️' },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    <div className="w-64 bg-white shadow-sm h-screen sticky top-0">
      <nav className="mt-8 px-4">
        <ul className="space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <li key={item.name}>
                <Link
                  to={item.href}
                  className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <span className="mr-3 text-lg">{item.icon}</span>
                  {item.name}
                </Link>
              </li>
            );
          })}
        </ul>
        
        {/* FIRE Progress Card */}
        <div className="mt-8 p-4 bg-gradient-to-r from-orange-400 to-red-500 rounded-lg text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Progresso FIRE</span>
            <span className="text-lg">🔥</span>
          </div>
          <div className="text-2xl font-bold mb-1">32%</div>
          <div className="w-full bg-white/20 rounded-full h-2">
            <div className="bg-white h-2 rounded-full" style={{ width: '32%' }}></div>
          </div>
          <div className="text-xs mt-2 opacity-90">
            8 anos restantes
          </div>
        </div>
        
        {/* Quick Stats */}
        <div className="mt-6 space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Este mês</span>
            <span className="font-semibold text-gray-900">R$ 4.580</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Taxa de poupança</span>
            <span className="font-semibold text-green-600">42%</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Meta FIRE</span>
            <span className="font-semibold text-blue-600">R$ 1.8M</span>
          </div>
        </div>
      </nav>
    </div>
  );
};