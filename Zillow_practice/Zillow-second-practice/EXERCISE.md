# Practice Exercise 2: Tour Scheduler

**Time box:** 60 minutes, out loud, no AI assistants or autocomplete.
**Goal:** build an in-memory service that schedules property **tours**
(visits where a buyer's agent shows a home to a buyer).
4 levels, each building on the previous one. Finish each level working
before moving on.

Write your code in `tour_scheduler.py` (same folder). Check each level with:

```
python test_tour_scheduler.py 1   # Level 1 only
python test_tour_scheduler.py 3   # Levels 1 to 3
```

Don't open the test file until you finish a level. Anything not stated
here: decide, and say your assumption out loud.

**Before you say "done" with a level:** reread every rule and ask
"what happens if…?" (ties, `None`, boundaries, exact limits).

---

## Level 1: Model and storage (~10 min)

- **`Agent`**: `agent_id`, `name`, `city`, with `Agent.from_dict(data)`.
- **`Property`**: `property_id`, `address`, `city`, with `Property.from_dict(data)`.
- **`TourScheduler`**:
  - `add_agent(agent)` / `add_property(property)`: `ValueError` on duplicate ID.
  - `get_agent(agent_id)` / `get_property(property_id)`: `KeyError` if missing.

## Level 2: Scheduling tours (~25 min)

- **`Tour`**: `tour_id`, `property_id`, `agent_id`, `buyer_name`,
  `start` (`datetime`), `duration_minutes` (int), plus its **end** time.
- `schedule_tour(tour_id, property_id, agent_id, buyer_name, start, duration_minutes=30) -> Tour`

  Raise `KeyError` if the property or agent doesn't exist. Raise `ValueError` if:
  1. `tour_id` already exists.
  2. The agent works in a different city than the property.
  3. `duration_minutes` is not between 15 and 120 (inclusive).
  4. The tour doesn't fit in business hours: it must start at or after 09:00
     and end at or before 18:00, on the same day.
  5. The **agent** already has a tour that overlaps this one.
  6. The **property** already has a tour that overlaps this one.

  Back-to-back tours are fine: a tour ending at 10:30 does not overlap
  one starting at 10:30.

- `get_agent_schedule(agent_id, day: date) -> list[Tour]`: that agent's tours
  on that day, earliest first. `KeyError` if the agent doesn't exist.

## Level 3: Cancellations and availability (~15 min)

- `cancel_tour(tour_id)`: `KeyError` if it doesn't exist, `ValueError` if it
  was already cancelled. A cancelled tour **frees its time slot** and no longer
  appears in schedules or counts.
- `find_available_agents(property_id, start, duration_minutes=30) -> list[str]`:
  IDs of agents in the property's city who are free for that slot, sorted by ID.
  If the **property** itself is already booked at that time, return `[]`.
- `busiest_agents(k) -> list[str]`: the `k` agents with the most scheduled
  (non-cancelled) tours. Ties by agent ID ascending. Agents with 0 tours count too.

## Level 4: Finding the next slot (~10 min, bonus)

- `next_available_slot(agent_id, property_id, day, duration_minutes=30) -> datetime | None`:
  the earliest start time on that day, on the half hour (09:00, 09:30, 10:00…),
  where both the agent and the property are free and the tour fits in business
  hours. `None` if there's no such slot. `ValueError` if agent and property are
  in different cities.

---

## Self-review after the 60 minutes

1. Where did you write the "do these two time ranges overlap?" logic? Only once?
2. How many places check "is this tour cancelled?"? Could it be one?
3. With 10,000 tours per agent, which method gets slow? What structure would
   help? (Just be ready to explain it.)
