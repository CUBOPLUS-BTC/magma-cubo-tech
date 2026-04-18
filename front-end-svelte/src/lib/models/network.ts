export interface NetworkStatus {
  fees: {
    fastestFee: number;
    halfHourFee: number;
    economyFee: number;
  };
  block_height: number;
  mempool_size: {
    count: number;
    vsize: number;
  };
}
