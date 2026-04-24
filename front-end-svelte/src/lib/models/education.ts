export type TimePreference = 'high' | 'mixed' | 'low';
export type LessonDifficulty = 'beginner' | 'intermediate' | 'advanced';

export interface LessonStatus {
  best_score: number;
  passed: boolean;
  perfect: boolean;
  attempts: number;
  last_attempt_at: number;
}

export interface UnitLesson {
  id: string;
  title: string;
  description: string;
  difficulty: LessonDifficulty;
  duration_min: number;
  quiz_count: number;
  status: LessonStatus;
}

export interface LearningUnit {
  id: string;
  title: string;
  subtitle: string;
  theme_color: string;
  icon: string;
  time_preference: TimePreference;
  lesson_ids: string[];
  lesson_count: number;
  lessons: UnitLesson[];
  unlocked: boolean;
  completed: boolean;
  progress_pct: number;
}

export interface UnitsResponse {
  locale: 'es' | 'en';
  units: LearningUnit[];
}

export interface LevelInfo {
  level: number;
  name_es: string;
  name_en: string;
  xp_current_level: number;
  xp_next_level: number;
  xp_into_level: number;
  xp_to_next_level: number;
  progress_pct: number;
  is_max_level: boolean;
}

export interface EducationState {
  pubkey: string;
  xp_total: number;
  hearts: number;
  hearts_max: number;
  hearts_last_refill_at: number;
  streak_days: number;
  streak_last_day: string | null;
  daily_xp_goal: number;
  daily_xp_today: number;
  daily_xp_day: string | null;
  created_at: number;
  updated_at: number;
  level: LevelInfo;
  next_heart_in_seconds: number;
  daily_goal_pct: number;
  daily_goal_met: boolean;
}

export interface ProgressResponse {
  state: EducationState;
  lesson_statuses: Record<string, LessonStatus>;
}

export interface LessonDetail {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: LessonDifficulty;
  duration_min: number;
  content: string;
  quiz: Array<{
    question: string;
    options: string[];
    explanation: string;
  }>;
  locale: 'es' | 'en';
}

export interface QuizResultItem {
  question_number: number;
  question: string;
  chosen_index: number;
  correct_index: number;
  is_correct: boolean;
  explanation: string;
}

export interface QuizProgressPayload {
  lesson_id: string;
  score_pct: number;
  passed: boolean;
  perfect: boolean;
  xp_earned: number;
  already_passed: boolean;
  hearts_lost: number;
  state: EducationState;
}

export interface QuizResult {
  lesson_id: string;
  locale: 'es' | 'en';
  score: {
    correct: number;
    total: number;
    percentage: number;
    passed: boolean;
    grade: string;
  };
  results: QuizResultItem[];
  progress?: QuizProgressPayload;
}
