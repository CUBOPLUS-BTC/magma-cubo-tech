"""Gamification (achievements + XP)."""

from __future__ import annotations

from ._base import Resource


class GamificationResource(Resource):
    def achievements(self) -> dict:
        """GET /achievements — requires auth."""
        return self._get("/achievements", auth=True)
