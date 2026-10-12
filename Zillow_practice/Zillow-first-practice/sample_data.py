"""Dummy listing data, shaped like a JSON payload from an API.

Dates are ISO strings and statuses are uppercase strings on purpose:
converting them into proper Python types is part of the exercise.
"""

LISTINGS = [
    {"listing_id": "L001", "address": "123 Pine St",      "city": "Seattle", "price": 850000,  "bedrooms": 3, "bathrooms": 2.0, "sqft": 1700, "status": "ACTIVE",     "listed_date": "2026-09-01"},
    {"listing_id": "L002", "address": "45 Lake Ave",      "city": "Seattle", "price": 1200000, "bedrooms": 4, "bathrooms": 3.0, "sqft": 2400, "status": "ACTIVE",     "listed_date": "2026-08-15"},
    {"listing_id": "L003", "address": "9 Rainier Way",    "city": "Seattle", "price": 640000,  "bedrooms": 2, "bathrooms": 1.0, "sqft": 1000, "status": "PENDING",    "listed_date": "2026-07-20"},
    {"listing_id": "L004", "address": "77 Broadway",      "city": "Denver",  "price": 525000,  "bedrooms": 3, "bathrooms": 2.0, "sqft": 1500, "status": "ACTIVE",     "listed_date": "2026-09-20"},
    {"listing_id": "L005", "address": "300 Colfax Ave",   "city": "Denver",  "price": 410000,  "bedrooms": 2, "bathrooms": 1.0, "sqft": 950,  "status": "ACTIVE",     "listed_date": "2026-06-30"},
    {"listing_id": "L006", "address": "18 Larimer St",    "city": "Denver",  "price": 780000,  "bedrooms": 4, "bathrooms": 3.0, "sqft": 2600, "status": "SOLD",       "listed_date": "2026-05-10"},
    {"listing_id": "L007", "address": "5 Congress Ave",   "city": "Austin",  "price": 495000,  "bedrooms": 3, "bathrooms": 2.0, "sqft": 1650, "status": "ACTIVE",     "listed_date": "2026-09-28"},
    {"listing_id": "L008", "address": "210 Rainey St",    "city": "Austin",  "price": 615000,  "bedrooms": 3, "bathrooms": 2.5, "sqft": 1800, "status": "ACTIVE",     "listed_date": "2026-08-01"},
    {"listing_id": "L009", "address": "64 South Lamar",   "city": "Austin",  "price": 389000,  "bedrooms": 2, "bathrooms": 2.0, "sqft": 1100, "status": "OFF_MARKET", "listed_date": "2026-04-12"},
    {"listing_id": "L010", "address": "12 Ocean Dr",      "city": "Austin",  "price": 495000,  "bedrooms": 3, "bathrooms": 2.0, "sqft": 1500, "status": "ACTIVE",     "listed_date": "2026-09-10"},
    {"listing_id": "L011", "address": "88 Capitol Hill",  "city": "Seattle", "price": 699000,  "bedrooms": 2, "bathrooms": 2.0, "sqft": 1150, "status": "ACTIVE",     "listed_date": "2026-10-01"},
    {"listing_id": "L012", "address": "3 Cherry Creek",   "city": "Denver",  "price": 1150000, "bedrooms": 5, "bathrooms": 4.0, "sqft": 3400, "status": "PENDING",    "listed_date": "2026-08-25"},
]

# Each of these must be rejected by add_listing with a ValueError.
INVALID_LISTINGS = [
    {"listing_id": "L001", "address": "Duplicate ID",     "city": "Seattle", "price": 500000,  "bedrooms": 2, "bathrooms": 1.0, "sqft": 900,  "status": "ACTIVE",     "listed_date": "2026-09-01"},
    {"listing_id": "L100", "address": "Negative price",   "city": "Austin",  "price": -1,      "bedrooms": 2, "bathrooms": 1.0, "sqft": 900,  "status": "ACTIVE",     "listed_date": "2026-09-01"},
    {"listing_id": "L101", "address": "Zero sqft",        "city": "Denver",  "price": 300000,  "bedrooms": 1, "bathrooms": 1.0, "sqft": 0,    "status": "ACTIVE",     "listed_date": "2026-09-01"},
    {"listing_id": "L102", "address": "Negative bedrooms","city": "Austin",  "price": 300000,  "bedrooms": -2, "bathrooms": 1.0, "sqft": 900, "status": "ACTIVE",     "listed_date": "2026-09-01"},
]
