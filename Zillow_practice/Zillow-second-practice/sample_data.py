"""Dummy data for the Tour Scheduler exercise.

Datetimes arrive as ISO strings ("2026-10-20T10:00"): converting them
is part of the exercise.
"""

AGENTS = [
    {"agent_id": "A1", "name": "Ana Torres",   "city": "Seattle"},
    {"agent_id": "A2", "name": "Ben Carter",   "city": "Seattle"},
    {"agent_id": "A3", "name": "Carla Ruiz",   "city": "Denver"},
    {"agent_id": "A4", "name": "Diego Flores", "city": "Austin"},
    {"agent_id": "A5", "name": "Eva Lin",      "city": "Austin"},
]

PROPERTIES = [
    {"property_id": "P1", "address": "123 Pine St",    "city": "Seattle"},
    {"property_id": "P2", "address": "45 Lake Ave",    "city": "Seattle"},
    {"property_id": "P3", "address": "77 Broadway",    "city": "Denver"},
    {"property_id": "P4", "address": "5 Congress Ave", "city": "Austin"},
    {"property_id": "P5", "address": "210 Rainey St",  "city": "Austin"},
    {"property_id": "P6", "address": "12 Ocean Dr",    "city": "Miami"},
]

# All valid: schedule them in this order to get the starting state used by the tests.
TOURS = [
    {"tour_id": "T1", "property_id": "P1", "agent_id": "A1", "buyer_name": "Lee",    "start": "2026-10-20T10:00", "duration_minutes": 30},
    {"tour_id": "T2", "property_id": "P2", "agent_id": "A1", "buyer_name": "Kim",    "start": "2026-10-20T10:30", "duration_minutes": 60},
    {"tour_id": "T3", "property_id": "P1", "agent_id": "A2", "buyer_name": "Park",   "start": "2026-10-20T13:00", "duration_minutes": 45},
    {"tour_id": "T4", "property_id": "P3", "agent_id": "A3", "buyer_name": "Gomez",  "start": "2026-10-20T09:00", "duration_minutes": 30},
    {"tour_id": "T5", "property_id": "P4", "agent_id": "A4", "buyer_name": "Smith",  "start": "2026-10-20T11:00", "duration_minutes": 30},
    {"tour_id": "T6", "property_id": "P5", "agent_id": "A4", "buyer_name": "Jones",  "start": "2026-10-20T15:00", "duration_minutes": 60},
    {"tour_id": "T7", "property_id": "P4", "agent_id": "A5", "buyer_name": "Nguyen", "start": "2026-10-20T16:00", "duration_minutes": 30},
    {"tour_id": "T8", "property_id": "P2", "agent_id": "A2", "buyer_name": "Brown",  "start": "2026-10-21T09:30", "duration_minutes": 30},
]
