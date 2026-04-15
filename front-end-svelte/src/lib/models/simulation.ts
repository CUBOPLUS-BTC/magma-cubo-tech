export interface DayAnalysis {
  wait_days: number;
  avg_return: number;
  std_dev: number;
  worst_case: number;
  best_case: number;
  risk_zone: 'low' | 'medium' | 'high';
}

export interface SimulationResult {
  daily_analysis: DayAnalysis[];
  recommendation: string;
  risk_level: string;
  optimal_day: number;
  expected_return: number;
}

export interface PurchaseStrategy {
  amount: number;
  risk: number;
  sharpe_ratio: number;
}

export interface DcaStrategy {
  amount_per_period: number;
  periods: number;
  risk: number;
}

export interface ConversionResult {
  strategy: string;
  explanation: string;
  lump_sum: PurchaseStrategy;
  dca: DcaStrategy;
}
