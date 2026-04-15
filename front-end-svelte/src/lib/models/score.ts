export interface ScoreBreakdown {
  consistency: number;
  relative_volume: number;
  diversification: number;
  savings_pattern: number;
  payment_history: number;
  lightning_activity: number;
}

export interface ScoreResult {
  total_score: number;
  rank: 'Excellent' | 'Good' | 'Fair' | 'Developing' | 'New';
  address: string;
  breakdown: ScoreBreakdown;
  recommendations: string[];
}
