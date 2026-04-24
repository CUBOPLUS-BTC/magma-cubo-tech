"""Unit (chapter) definitions for the learning path.

Lessons are grouped into narrative chapters that progress from "high time
preference thinking" (immediate gratification, fiat mindset) toward
"low time preference thinking" (patience, hard money, sovereignty).

Each unit has:
- ``id``: stable slug
- ``title_en`` / ``title_es``
- ``subtitle_en`` / ``subtitle_es`` — short framing line
- ``theme_color``: css token (amber, cyan, orange, etc.) for the path UI
- ``icon``: phosphor icon name the frontend renders
- ``lesson_ids``: ordered list of lesson slugs in this unit
- ``time_preference``: "high" | "mixed" | "low" — narrative tag
"""

from __future__ import annotations

UNITS: list[dict] = [
    {
        "id": "unit-money",
        "title_en": "What is money really?",
        "title_es": "¿Qué es el dinero de verdad?",
        "subtitle_en": "Break the fiat mindset. See money clearly.",
        "subtitle_es": "Rompé el molde fiat. Vé el dinero con claridad.",
        "theme_color": "amber",
        "icon": "Coins",
        "time_preference": "high",
        "lesson_ids": [
            "what-is-bitcoin",
        ],
    },
    {
        "id": "unit-foundations",
        "title_en": "Bitcoin foundations",
        "title_es": "Fundamentos de Bitcoin",
        "subtitle_en": "How the network actually works under the hood.",
        "subtitle_es": "Cómo funciona la red realmente por dentro.",
        "theme_color": "orange",
        "icon": "CurrencyBtc",
        "time_preference": "mixed",
        "lesson_ids": [
            "how-transactions-work",
            "understanding-utxos",
            "understanding-mempool",
            "understanding-fees",
        ],
    },
    {
        "id": "unit-low-time-preference",
        "title_en": "Low time preference",
        "title_es": "Baja preferencia temporal",
        "subtitle_en": "The hardest lesson: patience pays exponentially.",
        "subtitle_es": "La lección más dura: la paciencia paga exponencialmente.",
        "theme_color": "emerald",
        "icon": "PiggyBank",
        "time_preference": "low",
        "lesson_ids": [
            "saving-in-bitcoin",
            "halvings-and-supply",
        ],
    },
    {
        "id": "unit-sovereignty",
        "title_en": "Self-sovereignty",
        "title_es": "Auto-soberanía",
        "subtitle_en": "Your keys, your coins. Own it.",
        "subtitle_es": "Tus llaves, tus monedas. Hacete cargo.",
        "theme_color": "violet",
        "icon": "ShieldCheck",
        "time_preference": "low",
        "lesson_ids": [
            "multisig-wallets",
            "bitcoin-privacy",
            "running-a-node",
        ],
    },
    {
        "id": "unit-mining",
        "title_en": "Mining & consensus",
        "title_es": "Minería y consenso",
        "subtitle_en": "Proof of work — the anchor of truth.",
        "subtitle_es": "Prueba de trabajo — el ancla de la verdad.",
        "theme_color": "red",
        "icon": "Pickaxe",
        "time_preference": "mixed",
        "lesson_ids": [
            "mining-and-pow",
        ],
    },
    {
        "id": "unit-layers",
        "title_en": "Layers above Bitcoin",
        "title_es": "Capas sobre Bitcoin",
        "subtitle_en": "Scale without compromising the base layer.",
        "subtitle_es": "Escalá sin comprometer la capa base.",
        "theme_color": "yellow",
        "icon": "Lightning",
        "time_preference": "mixed",
        "lesson_ids": [
            "lightning-network",
            "segwit-optimization",
        ],
    },
    {
        "id": "unit-advanced",
        "title_en": "Advanced protocol",
        "title_es": "Protocolo avanzado",
        "subtitle_en": "Taproot, Schnorr, and what's next.",
        "subtitle_es": "Taproot, Schnorr, y lo que viene.",
        "theme_color": "cyan",
        "icon": "Cube",
        "time_preference": "low",
        "lesson_ids": [
            "taproot-schnorr",
        ],
    },
    {
        "id": "unit-elsalvador",
        "title_en": "Bitcoin in El Salvador",
        "title_es": "Bitcoin en El Salvador",
        "subtitle_en": "Legal tender, remittances, and the circular economy.",
        "subtitle_es": "Moneda de curso legal, remesas y economía circular.",
        "theme_color": "sky",
        "icon": "Flag",
        "time_preference": "mixed",
        "lesson_ids": [
            "bitcoin-remittances-el-salvador",
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def list_units(locale: str = "en") -> list[dict]:
    """Return all units with locale-specific title/subtitle fields flattened."""
    out = []
    for unit in UNITS:
        out.append({
            "id": unit["id"],
            "title": unit[f"title_{locale}"],
            "subtitle": unit[f"subtitle_{locale}"],
            "theme_color": unit["theme_color"],
            "icon": unit["icon"],
            "time_preference": unit["time_preference"],
            "lesson_ids": unit["lesson_ids"],
            "lesson_count": len(unit["lesson_ids"]),
        })
    return out


def get_unit(unit_id: str) -> dict | None:
    for unit in UNITS:
        if unit["id"] == unit_id:
            return unit
    return None


def get_unit_for_lesson(lesson_id: str) -> dict | None:
    for unit in UNITS:
        if lesson_id in unit["lesson_ids"]:
            return unit
    return None
