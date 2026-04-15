import type { Translations } from './en';

export const es: Translations = {
  nav: { home: 'Inicio', score: 'Score', simulator: 'Simulador', remittance: 'Remesas', logout: 'Salir' },
  home: {
    welcome: 'Inteligencia Financiera Bitcoin',
    quickActions: 'Acciones Rápidas',
    analyzeAddress: 'Analizar Dirección',
    volatilitySimulator: 'Simulador de Volatilidad',
    remittanceOptimizer: 'Optimizador de Remesas',
    dontTrust: 'No confíes, verifica',
  },
  price: { fromSources: 'de {count} fuentes', verified: 'Verificado' },
  score: {
    title: 'Score Bitcoin',
    enterAddress: 'Ingresa una dirección Bitcoin para analizar',
    verify: 'Verificar',
    recommendations: 'Recomendaciones',
  },
  simulator: {
    title: 'Simulador de Volatilidad',
    amount: 'Monto (USD)',
    period: 'Período de Análisis',
    run: 'Ejecutar Simulación',
    optimalDay: 'Día Óptimo',
    expectedReturn: 'Retorno Esperado',
    riskLevel: 'Nivel de Riesgo',
    recommendation: 'Recomendación',
  },
  remittance: {
    title: 'Optimizador de Remesas',
    amount: 'Monto (USD)',
    frequency: 'Frecuencia',
    compare: 'Comparar Canales',
    annualSavings: 'Ahorro Anual',
    bestTime: 'Mejor Momento para Enviar',
    recommended: 'Recomendado',
  },
  common: { loading: 'Cargando...', error: 'Error', retry: 'Reintentar', cancel: 'Cancelar', close: 'Cerrar' },
};
