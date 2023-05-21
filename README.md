# realestate-com-au-api

🏠 Python wrapper for the realestate.com.au API

## Installation

Using **Python >= 3.6**:

```bash
pip install -e git+https://github.com/tomquirk/realestate-com-au-api.git#egg=realestate_com_au_api
```

### Example usage

```python
from realestate_com_au import RealestateComAu

api = RealestateComAu()

# Get property listings
listings = api.search(locations=["seventeen seventy, qld 4677"], channel="buy", keywords=["tenant"], exclude_keywords=["pool"])
```

## Data classes

#### [Listing](/realestate_com_au/objects/listing.py#L6)

Data class for a listing. See [listing.py](/realestate_com_au/objects/listing.py#L6) for reference.

## Legal

This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by REA Group or any of its affiliates or subsidiaries. This is an independent and unofficial API. Use at your own risk.


### List of Price Ranges that are detected Wrong to FIX!!! (2022-Nov!!)

565-575K
something where instead of the - the world 'to' is used
$420-440K
$1.55 - $1.65 Best Offers By Mon 21st Nov at 10am
1050K to 1090K
from $1.199.000M
$209 - $239,000
690,000-720,000
$1.1-1.15m
$1M - $1.1M 

#### Previously Fixed
    test_txt = 'from $1.199.000M'