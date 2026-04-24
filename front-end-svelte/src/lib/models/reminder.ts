export type ReminderCadence = 'monthly' | 'biweekly' | 'custom';
export type ReminderChannel = 'webhook' | 'nostr_dm' | 'email';

export interface Reminder {
  id: number;
  pubkey: string;
  recipient_id: number;
  cadence: ReminderCadence;
  day_of_month: number;
  hour_local: number;
  timezone: string;
  channels: ReminderChannel[];
  paused: boolean;
  next_fire_at: number;
  last_fired_at: number | null;
  fire_count: number;
  created_at: number;
  updated_at: number;
}

export interface ReminderListResponse {
  reminders: Reminder[];
  total: number;
}

export interface ReminderResponse {
  reminder: Reminder;
  message?: string;
}

export interface ReminderCreateInput {
  recipient_id: number;
  cadence?: ReminderCadence;
  day_of_month?: number;
  hour_local?: number;
  timezone?: string;
  channels?: ReminderChannel[];
}

export interface ReminderEvent {
  id: number;
  reminder_id: number;
  channel: ReminderChannel;
  status: 'sent' | 'failed' | 'skipped';
  error: string | null;
  fired_at: number;
}

export interface ReminderEventListResponse {
  events: ReminderEvent[];
  total: number;
}

export interface SendInvoiceResponse {
  bolt11: string;
  deeplink: string;
  amount_usd: number;
  amount_sats: number;
  amount_msat: number;
  btc_price_usd: number;
  recipient: {
    id: number;
    name: string;
    lightning_address: string;
    country: string | null;
  };
}
