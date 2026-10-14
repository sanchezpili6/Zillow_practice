from dataclasses import dataclass
from datetime import date, datetime, timedelta, time
from sample_data import AGENTS, PROPERTIES, TOURS

@dataclass
class Agent:
    agent_id: str
    name: str
    city: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            agent_id = data["agent_id"],
            name = data["name"],
            city = data["city"]
        )

@dataclass
class Property: 
    property_id: str
    address: str
    city: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            property_id = data["property_id"],
            address = data["address"],
            city = data["city"]
        )

class TourScheduler: 
    def __init__(self):
        self.agents_map = {}
        self.properties_map = {}
        self.tours_map = {}

    def add_agent(self, agent):
        if agent.agent_id in self.agents_map: 
            raise ValueError("This agent id already exists")
        self.agents_map[agent.agent_id] = agent

    def add_property(self, prop):
        if prop.property_id in self.properties_map: 
            raise ValueError("This property id already exists")
        self.properties_map[prop.property_id] = prop

    def get_agent(self, agent_id):
        if agent_id not in self.agents_map: 
            raise KeyError("This agent_id does not exist")
        return self.agents_map[agent_id]

    def get_property(self, property_id):
        if property_id not in self.properties_map:
            raise KeyError("This property_id does not exist")
        return self.properties_map[property_id]

    def schedule_tour(self, tour_id, property_id, agent_id, buyer_name, start, duration_minutes=30):
        prop = self.get_property(property_id)
        agent = self.get_agent(agent_id)
        if not prop:
            raise KeyError("This property id does not exist")

        if not agent:
            raise KeyError("This agent id does not exist")

        if tour_id in self.tours_map:
            raise ValueError("This tour id already exists")

        if agent.city != prop.city: 
            raise ValueError("This agent does not work in that city")

        if duration_minutes < 15 or duration_minutes >120:
            raise ValueError("Duration must be between 15 and 120 minutes ")

        end_datetime = start + timedelta(minutes=duration_minutes)

        if end_datetime.date() != start.date(): 
            raise ValueError("The tour must end on the same day it starts")

        if start.time() < time(9,0,0) or end_datetime.time() > time(18,0,0):
            raise ValueError("Tours must happen during business hours (9:00 to 18:00)")

        tour_overlap = self.tour_overlap(start, end_datetime, agent_id, property_id)
        if tour_overlap[0]: 
            raise ValueError(tour_overlap[1])

        new_tour = Tour(tour_id, property_id, agent_id, buyer_name, start, duration_minutes)
        self.tours_map[tour_id] = new_tour
        return new_tour

    def tour_overlap(self, start, end , agent_id, property_id):
        agent_schedule = self.get_agent_schedule(agent_id, start.date())
        property_schedule = self.get_property_schedule(property_id, start.date())
        for tour in agent_schedule:
            tour_end_datetime = tour.start + timedelta(minutes=tour.duration_minutes)
            if start < tour_end_datetime and tour.start < end:
                return(True, "The agent already has a tour scheduled during this time")

        for tour in property_schedule:
            tour_end_datetime = tour.start + timedelta(minutes=tour.duration_minutes)
            if start < tour_end_datetime and tour.start < end:
                return(True, "The property already has a tour scheduled during this time")

        return(False, "")

    def get_agent_schedule(self, agent_id, day):
        if agent_id not in self.agents_map:
            raise KeyError("This agent does not exist")
        agent_schedule = []
        for tour in self.tours_map.values():
            if tour.agent_id == agent_id and tour.start.date() == day:
                agent_schedule.append(tour)
        ordered_tours = sorted(agent_schedule, key= lambda x:x.start)
        return ordered_tours

    def get_property_schedule(self, property_id, day):
        if property_id not in self.properties_map:
            raise KeyError("This property does not exist")
        property_schedule = []
        for tour in self.tours_map.values():
            if tour.property_id == property_id and tour.start.date() == day:
                property_schedule.append(tour)
        ordered_tours = sorted(property_schedule, key= lambda x:x.start)
        return ordered_tours

        

@dataclass
class Tour: 
    tour_id:str
    property_id:str
    agent_id:str
    buyer_name:str
    start: datetime
    duration_minutes: int = 30


if __name__ == "__main__":

    test_tour_scheduler = TourScheduler()

    for p in PROPERTIES: 
        property = Property.from_dict(p)
        test_tour_scheduler.add_property(property)

    for a in AGENTS: 
        agent = Agent.from_dict(a)
        test_tour_scheduler.add_agent(agent)


    print(test_tour_scheduler.schedule_tour("T1", "P1", "A1", "Lee", datetime.fromisoformat("2026-10-20T10:00"), 30))