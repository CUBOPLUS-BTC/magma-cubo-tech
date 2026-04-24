export interface Recipient {
  id: number;
  pubkey: string;
  name: string;
  lightning_address: string;
  country: string;
  default_amount_usd: number | null;
  min_sendable_msat: number | null;
  max_sendable_msat: number | null;
  created_at: number;
  updated_at: number;
}

export interface RecipientListResponse {
  recipients: Recipient[];
  total: number;
}

export interface RecipientResponse {
  recipient: Recipient;
  message?: string;
}

export interface RecipientCreateInput {
  name: string;
  lightning_address: string;
  country?: string;
  default_amount_usd?: number | null;
  skip_lnurl_check?: boolean;
}
