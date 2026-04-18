export interface Achievement {
  id: string;
  name: string;
  desc: string;
  xp: number;
  earned: boolean;
  awarded_at: number | null;
}

export interface AchievementsResponse {
  achievements: Achievement[];
  total_xp: number;
  level: number;
  next_level_xp: number | null;
  earned_count: number;
  total_count: number;
}
