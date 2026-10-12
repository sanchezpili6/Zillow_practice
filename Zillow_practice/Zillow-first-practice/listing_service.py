from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from sample_data import LISTINGS

class Status(Enum): 
    ACTIVE = 1
    PENDING = 2
    SOLD = 3
    OFF_MARKET = 4

@dataclass
class Listing: 
    listing_id:str
    address:str
    city:str
    price:int
    bedrooms:int
    bathrooms:int
    sqft:int
    status:Status
    listed_date:date
    price_changes: list

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            listing_id = data["listing_id"],
            address = data["address"],
            city = data["city"],
            price = data["price"],
            bedrooms = data["bedrooms"],
            bathrooms = data["bathrooms"],
            sqft = data["sqft"],
            status = Status[data["status"]],
            listed_date = datetime.strptime(data["listed_date"],"%Y-%m-%d").date(),
            price_changes = [(datetime.strptime(data["listed_date"],"%Y-%m-%d").date(), data["price"])]
        )
        


class ListingService:
    def __init__(self):
        self.listing_map = {}

    def add_listing(self, listing): 
        if listing.listing_id in self.listing_map:
            raise ValueError("ID already exists")
        if listing.price <= 0:
            raise ValueError("price can't be less or equal to 0")
        if listing.sqft <= 0:
            raise ValueError("sqft can't be less or equal to 0")
        if listing.bedrooms < 0:
            raise ValueError("bedrooms can't be less than 0")
        if listing.bathrooms < 0:
            raise ValueError("bathrooms can't be less than 0")

        self.listing_map[listing.listing_id]=listing

    def get_listing(self, listing_id): 
        if listing_id not in self.listing_map: 
            raise KeyError("This listing Id doesn't exist")
            
        return self.listing_map[listing_id]

    def search(self, city=None, min_price=None, max_price=None, min_bedrooms=None, statuses={Status.ACTIVE}, sort_by="price", descending=False):
        filtered_listings = self.listing_map
        if not statuses: statuses = {Status.ACTIVE}
        if city: 
            filtered_listings = self.filter_city(self.listing_map, city)
        
        if min_price:
            priced_filtered= self.filter_min_price(filtered_listings, min_price)
            filtered_listings = priced_filtered

        if max_price:
            priced_filtered= self.filter_max_price(filtered_listings, max_price)
            filtered_listings = priced_filtered

        if min_bedrooms:
            bedroom_filtered = self.filter_min_bedrooms(filtered_listings, min_bedrooms)
            filtered_listings = bedroom_filtered

        if statuses: 
            status_filtered = self.filter_status(filtered_listings, statuses)
            filtered_listings = status_filtered

        if sort_by:
            sorted_listings = self.sort_listings(filtered_listings, sort_by, descending)
            filtered_listings = sorted_listings

        return filtered_listings

    def filter_city(self, listings , city): 
        filtered_listings = {}
        for key, values in listings.items(): 
            if values.city.lower() == city.lower().strip():
                filtered_listings[key] = values
        return filtered_listings

    def filter_min_price(self, listings, min_price):
        new_listings = {k:v for k,v in listings.items() if v.price >= min_price}
        return new_listings

    def filter_max_price(self, listings, max_price):
            new_listings = {k:v for k,v in listings.items() if v.price <= max_price}
            return new_listings

    def filter_min_bedrooms(self, listings, min_bedrooms):
            new_listings = {k:v for k,v in listings.items() if v.bedrooms >= min_bedrooms}
            return new_listings

    def filter_status(self, listings, statuses):
        filtered_listings = {}
        for key, values in listings.items(): 
            for status in statuses: 
                if values.status == status:
                    filtered_listings[key] = values
        return filtered_listings

    def sort_listings(self, listings, sort_by, descending):  
        SORT_KEYS = {
            "price": lambda listing: listing.price,
            "listed_date": lambda listing: listing.listed_date,
            "price_per_sqft": lambda listing: listing.price / listing.sqft,
        }
        if sort_by not in SORT_KEYS:
            raise ValueError("sort_by must be price, listed_date or price_per_sqft")

        sorted_listings = sorted(listings.values(), key= lambda s: (SORT_KEYS[sort_by](s), s.listing_id))

        if descending: 
            return sorted(listings.values(), key= lambda s: (SORT_KEYS[sort_by](s), -int(s.listing_id[1:])), reverse=descending)
        return sorted_listings

    def price_per_sqft(self, listing_id): 
        listing = self.get_listing(listing_id)
        price_per_sqft = listing.price/listing.sqft
        return float("{:.2f}" .format(price_per_sqft))

    def average_price_by_city(self, statuses={Status.ACTIVE}):
        filtered_statuses = self.filter_status(self.listing_map, statuses)
        prices_by_city = self.prices_by_city(filtered_statuses)

        for city in prices_by_city:
            prices_len = len(prices_by_city[city])
            prices_sum = 0
            for p in prices_by_city[city]: 
                prices_sum += p
            prices_by_city[city] = float("{:.2f}" .format(prices_sum/prices_len))
        return prices_by_city

    def prices_by_city(self, listings): 
        prices_by_city = {}
        for l in listings:
            listing = self.get_listing(l)
            if listing.city not in prices_by_city: 
                prices_by_city[listing.city] = []
            prices_by_city[listing.city].append(listing.price)
        return prices_by_city

    def days_on_market(self, listing_id, as_of:date):
        listing = self.get_listing(listing_id)
        listing_date = listing.listed_date

        return (as_of - listing_date).days

    def top_value_listings(self, city, k):
        top_values = []
        city_active_listings = self.search(city= city, sort_by="price_per_sqft")
        top_values = [l.listing_id for l in city_active_listings[:k]]
        return top_values

    def update_price(self, listing_id, new_price, changed_on:date):
        if new_price <= 0:
            raise ValueError("new_price must be more than 0")

        listing = self.get_listing(listing_id)

        listing.price = new_price
        listing.price_changes.append((changed_on, new_price))

        return self.get_listing(listing_id)
    
    def get_price_history(self, listing_id): 
        listing = self.get_listing(listing_id)
        return list(listing.price_changes)

    def price_drops(self, min_percent):
        price_drops = []
        for key, values in self.listing_map.items(): 
            original_price = values.price_changes[0][1]
            latest_price = values.price_changes[-1][1]
            price_drop = float("{:.2f}" .format(100 - latest_price * 100 / original_price))
            if price_drop >= min_percent and values.status == Status.ACTIVE: 
                price_drops.append((key, price_drop))
        return sorted(price_drops, key= lambda x: (-x[1], x[0]))

    ALLOWED_TRANSITIONS = {
        Status.ACTIVE: {Status.PENDING, Status.OFF_MARKET},
        Status.PENDING: {Status.ACTIVE, Status.SOLD},
        Status.OFF_MARKET: {Status.ACTIVE},
        Status.SOLD: set()
    }

    def update_status(self, listing_id, new_status): 
        listing = self.get_listing(listing_id)
        if new_status not in self.ALLOWED_TRANSITIONS[listing.status]: 
            raise ValueError(f"Transition not allowed from {listing.status.name} to {new_status.name}")
        listing.status = new_status
        

        

test_listing_service = ListingService()

for l in LISTINGS: 
    listing = Listing.from_dict(l)
    test_listing_service.add_listing(listing)

test_listing_service.update_price("L002", 1100000, date(2026, 9, 10))
test_listing_service.update_price("L002", 1050000, date(2026, 9, 25))
test_listing_service.update_price("L008", 580000, date(2026, 9, 15))
test_listing_service.update_price("L004", 530000, date(2026, 9, 30))

print(test_listing_service.price_drops(5))
