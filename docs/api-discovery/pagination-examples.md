# Zephyr API Pagination Examples

**Date:** 2025-01-29  
**Status:** ✅ Verified from Official Documentation

---

## Pagination Parameters

- **Offset Parameter:** `firstresult` (zero-based, 0 = first record)
- **Limit Parameter:** `maxresults` (maximum items per request)

---

## Example Requests

### First Page (First 100 Records)

```
GET /flex/services/rest/latest/advancesearch?word=test&entitytype=testcase&releaseid=1&zql=false&firstresult=0&maxresults=100
```

### Second Page (Next 100 Records)

```
GET /flex/services/rest/latest/advancesearch?word=test&entitytype=testcase&releaseid=1&zql=false&firstresult=100&maxresults=100
```

### Third Page (Next 100 Records)

```
GET /flex/services/rest/latest/advancesearch?word=test&entitytype=testcase&releaseid=1&zql=false&firstresult=200&maxresults=100
```

---

## Pagination Logic

1. **Start:** Set `firstresult=0` to begin with the first record
2. **Page Size:** Set `maxresults` to desired page size (e.g., 100, 500)
3. **Next Page:** Increment `firstresult` by `maxresults` value
   - Page 1: `firstresult=0`
   - Page 2: `firstresult=100` (if `maxresults=100`)
   - Page 3: `firstresult=200` (if `maxresults=100`)

---

## Implementation Pattern

```python
def paginate_zephyr_api(endpoint, page_size=100):
    firstresult = 0
    maxresults = page_size

    while True:
        url = f"{base_url}{endpoint}?firstresult={firstresult}&maxresults={maxresults}"
        response = session.get(url)
        data = response.json()

        if not data or len(data) == 0:
            break

        yield data

        if len(data) < maxresults:
            break  # Last page

        firstresult += maxresults
```

---

## Important Notes

1. **Zero-Based:** `firstresult` is zero-based (0 = first record, not 1)
2. **Increment by Page Size:** Always increment `firstresult` by `maxresults` value
3. **Stop Condition:** Stop when response is empty or has fewer items than `maxresults`
4. **Not All Endpoints:** Some endpoints may not support pagination - test each endpoint

---

## Source

- **Official Documentation:** [Zephyr Enterprise REST API - Search API](https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-enterprise/zephyr-rest-api/search-api.html)
- **Verified:** 2025-01-29

---

**Last Updated:** 2025-01-29
