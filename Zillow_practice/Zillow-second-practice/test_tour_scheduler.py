"""Hidden test cases. Don't read until you finish a level!

Usage: python test_tour_scheduler.py [max_level]
"""
import sys
import traceback
from datetime import date, datetime

from sample_data import AGENTS, PROPERTIES, TOURS
from tour_scheduler import Agent, Property, TourScheduler

DAY = date(2026, 10, 20)


def at(hour, minute=0, day=DAY):
    return datetime(day.year, day.month, day.day, hour, minute)


def base_scheduler():
    scheduler = TourScheduler()
    for row in AGENTS:
        scheduler.add_agent(Agent.from_dict(row))
    for row in PROPERTIES:
        scheduler.add_property(Property.from_dict(row))
    return scheduler


def loaded_scheduler():
    scheduler = base_scheduler()
    for row in TOURS:
        scheduler.schedule_tour(row["tour_id"], row["property_id"], row["agent_id"],
                                row["buyer_name"], datetime.fromisoformat(row["start"]),
                                row["duration_minutes"])
    return scheduler


def ids(tours):
    return [tour.tour_id for tour in tours]


def expect_error(error_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"expected {error_type.__name__} from {func.__name__}{args}")


def test_level_1():
    scheduler = base_scheduler()
    assert scheduler.get_agent("A3").city == "Denver"
    assert scheduler.get_property("P6").address == "12 Ocean Dr"
    expect_error(ValueError, scheduler.add_agent, Agent.from_dict(AGENTS[0]))
    expect_error(ValueError, scheduler.add_property, Property.from_dict(PROPERTIES[0]))
    expect_error(KeyError, scheduler.get_agent, "A99")
    expect_error(KeyError, scheduler.get_property, "P99")


def test_level_2():
    scheduler = loaded_scheduler()
    tour = scheduler.schedule_tour("T9", "P1", "A1", "Diaz", at(11, 30))  # back-to-back with T2
    assert tour.tour_id == "T9" and tour.duration_minutes == 30
    assert ids(scheduler.get_agent_schedule("A1", DAY)) == ["T1", "T2", "T9"]
    assert ids(scheduler.get_agent_schedule("A2", DAY)) == ["T3"]  # T8 is the next day
    assert scheduler.get_agent_schedule("A5", date(2026, 10, 22)) == []
    expect_error(KeyError, scheduler.get_agent_schedule, "A99", DAY)

    expect_error(KeyError, scheduler.schedule_tour, "X1", "P99", "A1", "Doe", at(14))
    expect_error(KeyError, scheduler.schedule_tour, "X2", "P1", "A99", "Doe", at(14))
    expect_error(ValueError, scheduler.schedule_tour, "T1", "P1", "A1", "Doe", at(14))      # duplicate ID
    expect_error(ValueError, scheduler.schedule_tour, "X3", "P1", "A3", "Doe", at(14))      # Denver agent
    expect_error(ValueError, scheduler.schedule_tour, "X4", "P1", "A1", "Doe", at(14), 10)  # too short
    expect_error(ValueError, scheduler.schedule_tour, "X5", "P1", "A1", "Doe", at(14), 150) # too long
    expect_error(ValueError, scheduler.schedule_tour, "X6", "P1", "A1", "Doe", at(8, 30))   # too early
    expect_error(ValueError, scheduler.schedule_tour, "X7", "P1", "A1", "Doe", at(17, 45), 30)  # ends 18:15
    expect_error(ValueError, scheduler.schedule_tour, "X8", "P1", "A1", "Doe", at(11), 30)  # A1 busy (T2)
    expect_error(ValueError, scheduler.schedule_tour, "X9", "P1", "A2", "Doe", at(10, 15))  # P1 busy (T1)
    # exact limits are allowed
    scheduler.schedule_tour("T10", "P3", "A3", "Ok", at(17), 60)    # ends exactly 18:00
    scheduler.schedule_tour("T11", "P3", "A3", "Ok", at(12), 15)
    scheduler.schedule_tour("T12", "P3", "A3", "Ok", at(13), 120)
    assert ids(scheduler.get_agent_schedule("A3", DAY)) == ["T4", "T11", "T12", "T10"]


def test_level_3():
    scheduler = loaded_scheduler()
    assert scheduler.busiest_agents(3) == ["A1", "A2", "A4"]
    assert scheduler.busiest_agents(10) == ["A1", "A2", "A4", "A3", "A5"]

    scheduler.cancel_tour("T2")
    assert ids(scheduler.get_agent_schedule("A1", DAY)) == ["T1"]
    assert scheduler.busiest_agents(2) == ["A2", "A4"]
    expect_error(ValueError, scheduler.cancel_tour, "T2")
    expect_error(KeyError, scheduler.cancel_tour, "T99")
    scheduler.schedule_tour("T9", "P2", "A2", "Diaz", at(10, 30), 60)  # T2's old slot is free

    scheduler = loaded_scheduler()
    assert scheduler.find_available_agents("P1", at(11)) == ["A2"]           # A1 busy with T2
    assert scheduler.find_available_agents("P1", at(10, 15)) == []          # P1 itself is booked
    assert scheduler.find_available_agents("P5", at(11, 15)) == ["A5"]       # A4 busy with T5
    assert scheduler.find_available_agents("P2", at(14)) == ["A1", "A2"]
    assert scheduler.find_available_agents("P6", at(11)) == []               # no agents in Miami
    expect_error(KeyError, scheduler.find_available_agents, "P99", at(11))


def test_level_4():
    scheduler = loaded_scheduler()
    assert scheduler.next_available_slot("A1", "P1", DAY) == at(9)
    assert scheduler.next_available_slot("A1", "P2", DAY, 90) == at(11, 30)  # A1 busy 10:00-11:30
    assert scheduler.next_available_slot("A2", "P1", DAY, 90) == at(10, 30)  # P1 busy 10:00-10:30
    expect_error(ValueError, scheduler.next_available_slot, "A3", "P1", DAY)

    # Fill A3's day: 09:00-17:00 booked, only 17:00-18:00 left
    scheduler.cancel_tour("T4")
    for number, hour in enumerate([9, 11, 13, 15]):
        scheduler.schedule_tour(f"F{number}", "P3", "A3", "Full", at(hour), 120)
    assert scheduler.next_available_slot("A3", "P3", DAY, 60) == at(17)
    assert scheduler.next_available_slot("A3", "P3", DAY, 90) is None
    assert scheduler.next_available_slot("A3", "P3", date(2026, 10, 21), 120) == at(9, day=date(2026, 10, 21))


LEVELS = [test_level_1, test_level_2, test_level_3, test_level_4]

if __name__ == "__main__":
    max_level = int(sys.argv[1]) if len(sys.argv) > 1 else len(LEVELS)
    for number, test in enumerate(LEVELS[:max_level], start=1):
        try:
            test()
        except Exception as error:
            print(f"Level {number}: FAILED -> {type(error).__name__}: {error}")
            frame = next(f for f in reversed(traceback.extract_tb(error.__traceback__))
                         if f.filename.endswith("test_tour_scheduler.py"))
            print(f"  at line {frame.lineno}: {frame.line}")
            sys.exit(1)
        print(f"Level {number}: passed")
