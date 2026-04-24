"""Education progress + gamification layer.

State machine
-------------
- XP: earned per lesson completion. Feeds level progression.
- Hearts: 5 max. Lose one per wrong answer in quiz. Refill 1 heart every
  ``HEART_REFILL_SECONDS`` (4 hours). Cannot start a quiz with 0 hearts.
  This is the deliberate low-time-preference mechanic: you can't brute-force
  through mistakes, you must wait. Patience is literally the lesson.
- Streak: counts consecutive days the user earned >=1 XP. Resets if a day
  is skipped.
- Level: computed from XP_total using an exponential curve (see
  ``level_for_xp``). Each level has a Maxi-bitcoiner flavored name.

All times stored as UTC epoch seconds. "Day" is UTC YYYY-MM-DD string.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Optional

from ..database import _is_postgres, get_conn


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HEART_MAX = 5
HEART_REFILL_SECONDS = 4 * 60 * 60  # 4 hours
DAILY_XP_GOAL_DEFAULT = 30
PASSING_PCT = 60.0

# XP rewards (gentle curve — shipping matters more than grinding)
XP_FOR_LESSON_COMPLETE = 10       # baseline for completing a lesson
XP_FOR_QUIZ_PASS = 15             # passing the quiz
XP_FOR_PERFECT_QUIZ = 25          # 100% quiz bonus

# Level thresholds (cumulative XP) — Maxi bitcoiner progression.
# Each entry: (xp_required, name_es, name_en).
LEVEL_TABLE: list[tuple[int, str, str]] = [
    (0,     "Precoiner",       "Precoiner"),
    (30,    "Nocoiner curioso","Curious nocoiner"),
    (80,    "Plebeyo",         "Pleb"),
    (160,   "HODLer",          "HODLer"),
    (280,   "Stacker",         "Stacker"),
    (450,   "Bitcoiner",       "Bitcoiner"),
    (700,   "Maxi",            "Maxi"),
    (1000,  "Ciberhornet",     "Cyber hornet"),
    (1500,  "Satoshi-in-training", "Satoshi-in-training"),
    (2500,  "Toxic Maxi",      "Toxic Maxi"),
]


# ---------------------------------------------------------------------------
# Level helpers
# ---------------------------------------------------------------------------

def level_for_xp(xp: int) -> dict:
    """Return level info dict for the given XP total.

    Fields: ``level`` (1-based), ``name_es``, ``name_en``, ``xp_current_level``,
    ``xp_next_level``, ``xp_into_level``, ``progress_pct``.
    """
    level_idx = 0
    for i, (threshold, _, _) in enumerate(LEVEL_TABLE):
        if xp >= threshold:
            level_idx = i
        else:
            break

    current_threshold, name_es, name_en = LEVEL_TABLE[level_idx]
    next_threshold = (
        LEVEL_TABLE[level_idx + 1][0]
        if level_idx + 1 < len(LEVEL_TABLE)
        else current_threshold
    )

    into_level = xp - current_threshold
    span = max(1, next_threshold - current_threshold)
    progress_pct = round(min(1.0, into_level / span) * 100, 1)

    return {
        "level": level_idx + 1,
        "name_es": name_es,
        "name_en": name_en,
        "xp_current_level": current_threshold,
        "xp_next_level": next_threshold,
        "xp_into_level": into_level,
        "xp_to_next_level": max(0, next_threshold - xp),
        "progress_pct": progress_pct,
        "is_max_level": level_idx + 1 == len(LEVEL_TABLE),
    }


def _today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _yesterday_utc(day: str) -> str:
    try:
        d = datetime.strptime(day, "%Y-%m-%d")
    except Exception:
        return ""
    return (d.replace(tzinfo=timezone.utc) - _ONE_DAY).strftime("%Y-%m-%d")


from datetime import timedelta as _td
_ONE_DAY = _td(days=1)


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class EducationProgressManager:
    """CRUD + gamification rules for the education module."""

    # ------------------------------------------------------------------
    # State fetch / ensure
    # ------------------------------------------------------------------

    def get_state(self, pubkey: str) -> dict:
        """Return the gamification state for *pubkey*, creating it if absent."""
        if not pubkey:
            raise ValueError("pubkey requerido")
        row = self._fetch_state_row(pubkey)
        if row is None:
            return self._create_state(pubkey)
        state = self._row_to_state(row)
        state = self._apply_heart_refill(state)
        state = self._apply_daily_reset(state)
        return self._enrich(state)

    def _fetch_state_row(self, pubkey: str):
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        return conn.execute(
            f"SELECT * FROM education_state WHERE pubkey = {ph}", (pubkey,)
        ).fetchone()

    def _create_state(self, pubkey: str) -> dict:
        now = int(time.time())
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        conn.execute(
            f"""
            INSERT INTO education_state (
                pubkey, xp_total, hearts, hearts_max, hearts_last_refill_at,
                streak_days, streak_last_day, daily_xp_goal, daily_xp_today,
                daily_xp_day, created_at, updated_at
            ) VALUES ({', '.join([ph] * 12)})
            """,
            (
                pubkey, 0, HEART_MAX, HEART_MAX, now,
                0, None, DAILY_XP_GOAL_DEFAULT, 0,
                _today_utc(), now, now,
            ),
        )
        conn.commit()
        return self._enrich(self._row_to_state(self._fetch_state_row(pubkey)))

    # ------------------------------------------------------------------
    # Heart refill: +1 heart per HEART_REFILL_SECONDS elapsed
    # ------------------------------------------------------------------

    def _apply_heart_refill(self, state: dict) -> dict:
        if state["hearts"] >= state["hearts_max"]:
            # Keep refill timer pinned to now so the clock restarts next time.
            if state["hearts_last_refill_at"] == 0:
                self._save_state(state["pubkey"], hearts_last_refill_at=int(time.time()))
                state["hearts_last_refill_at"] = int(time.time())
            return state

        now = int(time.time())
        elapsed = now - (state["hearts_last_refill_at"] or now)
        if elapsed <= 0:
            return state

        refills = elapsed // HEART_REFILL_SECONDS
        if refills <= 0:
            return state

        new_hearts = min(state["hearts_max"], state["hearts"] + refills)
        # Anchor the refill clock to the last completed refill instant so
        # fractional progress is not lost.
        new_anchor = state["hearts_last_refill_at"] + refills * HEART_REFILL_SECONDS
        state["hearts"] = new_hearts
        state["hearts_last_refill_at"] = new_anchor
        self._save_state(
            state["pubkey"],
            hearts=new_hearts,
            hearts_last_refill_at=new_anchor,
        )
        return state

    # ------------------------------------------------------------------
    # Daily XP reset at UTC midnight
    # ------------------------------------------------------------------

    def _apply_daily_reset(self, state: dict) -> dict:
        today = _today_utc()
        if state["daily_xp_day"] != today:
            state["daily_xp_today"] = 0
            state["daily_xp_day"] = today
            self._save_state(
                state["pubkey"],
                daily_xp_today=0,
                daily_xp_day=today,
            )
        return state

    # ------------------------------------------------------------------
    # XP + streak accrual
    # ------------------------------------------------------------------

    def add_xp(self, pubkey: str, amount: int) -> dict:
        """Add XP, update streak, return enriched state."""
        if amount <= 0:
            return self.get_state(pubkey)

        state = self.get_state(pubkey)

        today = _today_utc()
        last_day = state["streak_last_day"]

        if last_day is None:
            new_streak = 1
        elif last_day == today:
            new_streak = state["streak_days"]  # already counted today
        else:
            yesterday = _yesterday_utc(today)
            if last_day == yesterday:
                new_streak = state["streak_days"] + 1
            else:
                new_streak = 1  # broken streak

        new_xp_total = state["xp_total"] + amount
        new_daily = state["daily_xp_today"] + amount

        self._save_state(
            pubkey,
            xp_total=new_xp_total,
            streak_days=new_streak,
            streak_last_day=today,
            daily_xp_today=new_daily,
        )

        state["xp_total"] = new_xp_total
        state["streak_days"] = new_streak
        state["streak_last_day"] = today
        state["daily_xp_today"] = new_daily
        return self._enrich(state)

    # ------------------------------------------------------------------
    # Hearts: lose / spend
    # ------------------------------------------------------------------

    def lose_heart(self, pubkey: str, count: int = 1) -> dict:
        """Spend ``count`` hearts. Never go below zero."""
        if count <= 0:
            return self.get_state(pubkey)
        state = self.get_state(pubkey)
        new_hearts = max(0, state["hearts"] - count)
        # If user JUST lost a heart at full, start the refill clock.
        new_anchor = state["hearts_last_refill_at"]
        if state["hearts"] == state["hearts_max"] and new_hearts < state["hearts_max"]:
            new_anchor = int(time.time())
        self._save_state(
            pubkey,
            hearts=new_hearts,
            hearts_last_refill_at=new_anchor,
        )
        state["hearts"] = new_hearts
        state["hearts_last_refill_at"] = new_anchor
        return self._enrich(state)

    # ------------------------------------------------------------------
    # Lesson completion record
    # ------------------------------------------------------------------

    def record_lesson_complete(
        self,
        pubkey: str,
        lesson_id: str,
        score_pct: float,
        hearts_lost: int = 0,
    ) -> dict:
        """Record a lesson completion, award XP, and return updated state.

        Idempotent-ish: a user can retake a lesson; each attempt is a row.
        XP is only awarded the first time the user ``passes`` (>=60%) a lesson.
        Subsequent attempts get a small XP bonus only on perfect runs.
        """
        if not pubkey:
            raise ValueError("pubkey requerido")
        if not lesson_id:
            raise ValueError("lesson_id requerido")

        now = int(time.time())
        is_pass = score_pct >= PASSING_PCT
        is_perfect = score_pct >= 99.9

        # Determine XP award
        already_passed = self._has_passed(pubkey, lesson_id)
        xp_earned = 0
        if is_pass and not already_passed:
            xp_earned = XP_FOR_LESSON_COMPLETE + XP_FOR_QUIZ_PASS
            if is_perfect:
                xp_earned += XP_FOR_PERFECT_QUIZ
        elif is_perfect and already_passed:
            xp_earned = 5  # small retake bonus for perfect runs

        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        conn.execute(
            f"""
            INSERT INTO education_progress
                (pubkey, lesson_id, score_pct, xp_earned, hearts_lost, completed_at)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            """,
            (pubkey, lesson_id, float(score_pct), int(xp_earned), int(hearts_lost), now),
        )
        conn.commit()

        state = self.get_state(pubkey)
        if xp_earned > 0:
            state = self.add_xp(pubkey, xp_earned)

        return {
            "lesson_id": lesson_id,
            "score_pct": score_pct,
            "passed": is_pass,
            "perfect": is_perfect,
            "xp_earned": xp_earned,
            "already_passed": already_passed,
            "hearts_lost": hearts_lost,
            "state": state,
        }

    def _has_passed(self, pubkey: str, lesson_id: str) -> bool:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        row = conn.execute(
            f"""
            SELECT 1 FROM education_progress
            WHERE pubkey = {ph} AND lesson_id = {ph} AND score_pct >= {ph}
            LIMIT 1
            """,
            (pubkey, lesson_id, PASSING_PCT),
        ).fetchone()
        return row is not None

    # ------------------------------------------------------------------
    # Per-lesson status (for the path UI)
    # ------------------------------------------------------------------

    def lesson_statuses(self, pubkey: str) -> dict[str, dict]:
        """Return per-lesson stats: best_score, passed, perfect, attempts."""
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        rows = conn.execute(
            f"""
            SELECT lesson_id,
                   MAX(score_pct) AS best_score,
                   COUNT(*) AS attempts,
                   MAX(completed_at) AS last_attempt_at
            FROM education_progress
            WHERE pubkey = {ph}
            GROUP BY lesson_id
            """,
            (pubkey,),
        ).fetchall()

        result: dict[str, dict] = {}
        for row in rows:
            if hasattr(row, "keys"):
                d = dict(row)
            else:
                d = dict(zip(
                    ["lesson_id", "best_score", "attempts", "last_attempt_at"],
                    row,
                ))
            best = float(d["best_score"] or 0)
            result[d["lesson_id"]] = {
                "best_score": round(best, 1),
                "passed": best >= PASSING_PCT,
                "perfect": best >= 99.9,
                "attempts": int(d["attempts"] or 0),
                "last_attempt_at": int(d["last_attempt_at"] or 0),
            }
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _save_state(self, pubkey: str, **fields) -> None:
        if not fields:
            return
        ph = "%s" if _is_postgres() else "?"
        set_parts = [f"{k} = {ph}" for k in fields.keys()]
        set_parts.append(f"updated_at = {ph}")
        params = list(fields.values()) + [int(time.time()), pubkey]
        conn = get_conn()
        conn.execute(
            f"UPDATE education_state SET {', '.join(set_parts)} WHERE pubkey = {ph}",
            params,
        )
        conn.commit()

    @staticmethod
    def _row_to_state(row) -> dict:
        if hasattr(row, "keys"):
            d = dict(row)
        else:
            cols = [
                "pubkey", "xp_total", "hearts", "hearts_max",
                "hearts_last_refill_at", "streak_days", "streak_last_day",
                "daily_xp_goal", "daily_xp_today", "daily_xp_day",
                "created_at", "updated_at",
            ]
            d = dict(zip(cols, row))
        return d

    @staticmethod
    def _enrich(state: dict) -> dict:
        """Add computed fields: level info, heart refill countdown, goal progress."""
        xp = int(state.get("xp_total", 0))
        level = level_for_xp(xp)

        hearts = int(state.get("hearts", 0))
        hearts_max = int(state.get("hearts_max", HEART_MAX))
        anchor = int(state.get("hearts_last_refill_at", 0))
        if hearts >= hearts_max:
            next_heart_in = 0
        else:
            now = int(time.time())
            elapsed = max(0, now - anchor)
            next_heart_in = max(0, HEART_REFILL_SECONDS - (elapsed % HEART_REFILL_SECONDS))

        daily_goal = int(state.get("daily_xp_goal", DAILY_XP_GOAL_DEFAULT))
        daily_today = int(state.get("daily_xp_today", 0))
        goal_pct = round(min(1.0, daily_today / max(1, daily_goal)) * 100, 1)

        return {
            **state,
            "level": level,
            "next_heart_in_seconds": next_heart_in,
            "daily_goal_pct": goal_pct,
            "daily_goal_met": daily_today >= daily_goal,
        }
