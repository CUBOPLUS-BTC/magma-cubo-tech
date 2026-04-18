export interface PensionProjection {
  total_invested_usd: number;
  total_btc_accumulated: number;
  current_value_usd: number;
  avg_buy_price: number;
  current_btc_price: number;
  monthly_breakdown: {
    month: number;
    invested: number;
    btc_bought: number;
    btc_total: number;
    value_usd: number;
  }[];
  monthly_data: {
    month: number;
    invested: number;
    traditional_value: number;
    btc_value: number;
  }[];
}
