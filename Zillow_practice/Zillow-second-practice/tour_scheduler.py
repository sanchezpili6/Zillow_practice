from dataclasses import dataclass
from datetime import date, datetime

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

    def add_agent(self, agent):
        if agent.agent_id in self.agents_map: 
            raise ValueError("This agent id already exists")
        self.agents_map[agent.agent_id] = agent

    def add_property(self, property):
        if property.property_id in self.properties_map: 
            raise ValueError("This property id already exists")
        self.properties_map[property.property_id] = property

    def get_agent(self, agent_id):
        if agent_id not in self.agents_map: 
            raise KeyError("This agent_id does not exist")
        return self.agents_map[agent_id]

    def get_property(self, property_id):
        if property_id not in self.properties_map:
            raise KeyError("This property_id does not exist")
        return self.properties_map[property_id]

@dataclass
class Tour: 
    tour_id:str
    property_id:str
    agent_id:str
    buyer_name:str
    start: datetime
    duration_minutes: int = 30

