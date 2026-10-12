# Practice Exercise: Listing Service

**Time box:** 60 minutes, out loud, no AI assistants or autocomplete.
**Goal:** build an in-memory service that manages real estate listings.
The exercise comes in 4 levels, each building on the previous one. Finish
each level working before moving on: a complete Level 2 beats a broken Level 4.

Write your code in `listing_service.py` (same folder). When you finish a level, run:

```
python test_listing_service.py 1   # checks Level 1 only
python test_listing_service.py 3   # checks Levels 1 to 3
python test_listing_service.py     # checks everything
```

Don't open the test file before you finish a level: treat it like the
interviewer's hidden test cases. Read only this spec, and decide anything
not stated here yourself (and say your assumption out loud).

---

## Level 1: Model and storage (~15 min)

Create in `listing_service.py`:

**`Status`**: an `Enum` with `ACTIVE`, `PENDING`, `SOLD`, `OFF_MARKET`.

**`Listing`**: one property for sale, with these fields:
`listing_id` (str), `address` (str), `city` (str), `price` (int, USD),
`bedrooms` (int), `bathrooms` (float), `sqft` (int), `status` (`Status`),
`listed_date` (`datetime.date`).

- `Listing.from_dict(data: dict) -> Listing`: builds a Listing from a raw dict
  like the ones in `sample_data.py` (status and date arrive as strings).

**`ListingService`**:
- `add_listing(listing)`: stores it. Raises `ValueError` if the ID already
  exists, or if `price <= 0`, `sqft <= 0`, `bedrooms < 0` or `bathrooms < 0`.
- `get_listing(listing_id) -> Listing`: raises `KeyError` if it doesn't exist.

## Level 2: Search (~20 min)

- `search(city=None, min_price=None, max_price=None, min_bedrooms=None,
  statuses=None, sort_by="price", descending=False) -> list[Listing]`
  - Every filter is optional; `None` means "don't filter by this".
  - `city` matching is case-insensitive and ignores surrounding spaces.
  - Price bounds are inclusive.
  - `statuses` is a set of `Status`; when `None`, only `ACTIVE` listings are returned.
  - `sort_by` is one of `"price"`, `"listed_date"`, `"price_per_sqft"`.
    Any other value raises `ValueError`.
  - **Ties are always broken by `listing_id` ascending**, even when `descending=True`.
  - No matches returns an empty list, not an error.

## Level 3: Market stats (~15 min)

- `price_per_sqft(listing_id) -> float`, rounded to 2 decimals.
- `average_price_by_city(statuses=None) -> dict[str, float]`: average price per
  city, rounded to 2 decimals. Default: `ACTIVE` only. Cities with no matching
  listings are not included.
- `days_on_market(listing_id, as_of: date) -> int`: days since `listed_date`.
- `top_value_listings(city, k) -> list[str]`: IDs of the `k` ACTIVE listings in
  that city with the **lowest** price per sqft (best value), ties by ID.
  If fewer than `k` exist, return all of them.

## Level 4: Price history and status rules (~10 min, bonus)

- `update_price(listing_id, new_price, changed_on: date)`: updates the price
  and records the change. `ValueError` if `new_price <= 0`.
- `get_price_history(listing_id) -> list[tuple[date, int]]`: oldest first,
  starting with `(listed_date, original_price)`.
- `price_drops(min_percent) -> list[tuple[str, float]]`: ACTIVE listings whose
  current price is at least `min_percent`% below their **original** price, as
  `(listing_id, percent_drop)` with `percent_drop` rounded to 2 decimals.
  Biggest drop first; ties by ID.
- `update_status(listing_id, new_status)`: only these transitions are allowed;
  anything else raises `ValueError`:

  | From       | To                 |
  |------------|--------------------|
  | ACTIVE     | PENDING, OFF_MARKET |
  | PENDING    | ACTIVE, SOLD       |
  | OFF_MARKET | ACTIVE             |
  | SOLD       | (final, none)      |

---

## After the 60 minutes (self-review)

1. Could a teammate understand each method without your explanation?
2. Is any method longer than ~15 lines? Could it be split?
3. If there were 10 million listings, which method would be slowest? What
   index would you add? (Just be able to explain it.)
4. What did you have to look up? Write it down: that's tomorrow's review list.
