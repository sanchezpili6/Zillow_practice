"""Hidden test cases. Don't read until you finish a level!

Usage: python test_listing_service.py [max_level]
"""
import sys
import traceback
from datetime import date

from listing_service import Listing, ListingService, Status
from sample_data import LISTINGS, INVALID_LISTINGS


def loaded_service():
    service = ListingService()
    for row in LISTINGS:
        service.add_listing(Listing.from_dict(row))
    return service


def ids(listings):
    return [listing.listing_id for listing in listings]


def expect_error(error_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"expected {error_type.__name__} from {func.__name__}{args}")


def test_level_1():
    service = loaded_service()
    listing = service.get_listing("L008")
    assert listing.city == "Austin"
    assert listing.price == 615000
    assert listing.bathrooms == 2.5
    assert listing.status == Status.ACTIVE, "status should be a Status enum"
    assert listing.listed_date == date(2026, 8, 1), "listed_date should be a date"

    for row in INVALID_LISTINGS:
        expect_error(ValueError, service.add_listing, Listing.from_dict(row))
    assert service.get_listing("L001").address == "123 Pine St", "duplicate must not overwrite"
    expect_error(KeyError, service.get_listing, "NOPE")


def test_level_2():
    service = loaded_service()
    assert ids(service.search()) == ["L005", "L007", "L010", "L004", "L008", "L011", "L001", "L002"]
    assert ids(service.search(city="  seattle ")) == ["L011", "L001", "L002"]
    assert ids(service.search(min_price=495000, max_price=699000)) == ["L007", "L010", "L004", "L008", "L011"]
    assert ids(service.search(min_bedrooms=3, sort_by="listed_date", descending=True)) == \
        ["L007", "L004", "L010", "L001", "L002", "L008"]
    # L007 and L010 share a price: ID ascending even when descending=True
    assert ids(service.search(city="Austin", descending=True)) == ["L008", "L007", "L010"]
    assert ids(service.search(statuses={Status.PENDING, Status.SOLD})) == ["L003", "L006", "L012"]
    # L001 and L002 share 500.0 per sqft
    assert ids(service.search(sort_by="price_per_sqft")) == \
        ["L007", "L010", "L008", "L004", "L005", "L001", "L002", "L011"]
    assert service.search(city="Miami") == []
    expect_error(ValueError, service.search, sort_by="bedrooms")


def test_level_3():
    service = loaded_service()
    assert service.price_per_sqft("L001") == 500.0
    assert service.price_per_sqft("L011") == 607.83
    assert service.average_price_by_city() == {"Seattle": 916333.33, "Denver": 467500.0, "Austin": 535000.0}
    assert service.average_price_by_city(statuses={Status.PENDING, Status.SOLD}) == \
        {"Seattle": 640000.0, "Denver": 965000.0}
    assert service.days_on_market("L005", date(2026, 10, 6)) == 98
    assert service.days_on_market("L011", date(2026, 10, 6)) == 5
    assert service.top_value_listings("Austin", 2) == ["L007", "L010"]
    assert service.top_value_listings("denver", 5) == ["L004", "L005"]  # only 2 active
    expect_error(KeyError, service.price_per_sqft, "NOPE")


def test_level_4():
    service = loaded_service()
    service.update_price("L002", 1100000, date(2026, 9, 10))
    service.update_price("L002", 1050000, date(2026, 9, 25))
    service.update_price("L008", 580000, date(2026, 9, 15))
    service.update_price("L004", 530000, date(2026, 9, 30))  # a price increase
    expect_error(ValueError, service.update_price, "L001", 0, date(2026, 10, 1))

    assert service.get_listing("L002").price == 1050000
    assert service.get_price_history("L002") == [
        (date(2026, 8, 15), 1200000), (date(2026, 9, 10), 1100000), (date(2026, 9, 25), 1050000)]
    assert service.get_price_history("L005") == [(date(2026, 6, 30), 410000)]
    assert service.price_drops(5) == [("L002", 12.5), ("L008", 5.69)]
    assert service.price_drops(10) == [("L002", 12.5)]

    service.update_status("L001", Status.PENDING)
    service.update_status("L001", Status.SOLD)
    expect_error(ValueError, service.update_status, "L001", Status.ACTIVE)  # SOLD is final
    expect_error(ValueError, service.update_status, "L005", Status.SOLD)    # must go through PENDING
    service.update_status("L009", Status.ACTIVE)
    assert "L009" in ids(service.search(city="Austin"))
    # L002 dropped 12.5% but is no longer ACTIVE
    service.update_status("L002", Status.PENDING)
    assert service.price_drops(5) == [("L008", 5.69)]


LEVELS = [test_level_1, test_level_2, test_level_3, test_level_4]

if __name__ == "__main__":
    max_level = int(sys.argv[1]) if len(sys.argv) > 1 else len(LEVELS)
    for number, test in enumerate(LEVELS[:max_level], start=1):
        try:
            test()
        except Exception as error:
            print(f"Level {number}: FAILED -> {type(error).__name__}: {error}")
            frame = traceback.extract_tb(error.__traceback__)[-1]
            if isinstance(error, AssertionError):
                frame = next(f for f in reversed(traceback.extract_tb(error.__traceback__))
                             if f.filename.endswith("test_listing_service.py"))
            print(f"  at line {frame.lineno}: {frame.line}")
            sys.exit(1)
        print(f"Level {number}: passed")