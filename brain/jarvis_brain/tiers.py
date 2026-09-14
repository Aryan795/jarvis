"""Risk tiers. The single place that decides how much ceremony an action needs.

From the review, section 2.6 and 3.5. The tier of a candidate action governs the guard
chain's behaviour and whether the action may appear in the satellite's on-device table.
"""

from __future__ import annotations

import enum


class Tier(enum.IntEnum):
    """Ordered by consequence. Higher means more ceremony before acting."""

    A = 0
    """Reversible, low consequence: lights, scenes, media volume.

    Act, then say what was done. Eligible for the satellite's on-device command table.
    """

    B = 1
    """Has a setpoint or a cost: climate, water heater, covers, notifications.

    Announce the action including its slot value, wait a short window, then act. The
    announcement must echo the number ("setting the bedroom AC to 18") so a wrong quantity
    is caught in the window, the same way a wrong polarity is (review 2.6).
    """

    C = 2
    """Security or safety: locks, gates, the alarm panel, anything irreversible.

    Confirm out loud and require an affirmative reply. Never acted on without a round trip,
    never eligible for the on-device table, never reachable from HA's built-in agent
    because the brain is the pipeline's only conversation agent (review 2.1).
    """


#: Domain to default tier. A specific entity may be promoted but never demoted.
DOMAIN_TIERS: dict[str, Tier] = {
    "light": Tier.A,
    "switch": Tier.A,
    "scene": Tier.A,
    "script": Tier.A,
    "fan": Tier.A,
    "media_player": Tier.A,
    "climate": Tier.B,
    "water_heater": Tier.B,
    "cover": Tier.B,
    "vacuum": Tier.B,
    "humidifier": Tier.B,
    "lock": Tier.C,
    "alarm_control_panel": Tier.C,
    "valve": Tier.C,
}

#: Entities that override their domain's tier upward. Loaded from config in practice.
ENTITY_TIER_OVERRIDES: dict[str, Tier] = {}


def tier_for(entity_id: str) -> Tier:
    """Return the tier for an entity, defaulting unknown domains to the safest tier.

    An unknown domain is tier C on purpose. A new integration should not be able to widen
    the blast radius by being unlisted.
    """
    if entity_id in ENTITY_TIER_OVERRIDES:
        return ENTITY_TIER_OVERRIDES[entity_id]
    domain = entity_id.split(".", 1)[0]
    return DOMAIN_TIERS.get(domain, Tier.C)
