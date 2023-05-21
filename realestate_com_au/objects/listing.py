from dataclasses import dataclass, field
import re
from realestate_com_au.utils import delete_nulls


@dataclass
class Listing:
    id: str
    badge: str                                              #Captures Promotional text not held elsewhere, such as 'Under Contract'
    url: str
    suburb: str
    state: str
    postcode: str
    short_address: str
    full_address: str
    property_type: str
    price: int
    price_text: str                                         #Captures the original text, such as a price range or comment. This is lost when converting to Integer
    bedrooms: int
    bathrooms: int
    parking_spaces: int
    building_size: int
    building_size_unit: str
    land_size: int
    land_size_unit: str
    listing_company_id: str
    listing_company_name: str
    listing_company_phone: str
    auction_date: str
    sold_date: str
    description: str
    images: list = field(default_factory=list)              #Captures Links to the photographic media
    images_floorplans: list = field(default_factory=list)   #Captures Links to the floorplans
    listers: list = field(default_factory=list)


@dataclass
class Lister:
    id: str
    name: str
    agent_id: str
    job_title: str
    url: str
    phone: str
    email: str

@dataclass
class MediaItem:
    link: str

def parse_price_text(range_str):

    # Remove non-digit characters and convert 'M' to '000000'
    range_str = re.sub(r'[^\d.-]', '', range_str)
    range_str = range_str.replace('M', '000000')
    
    # Extract lower and higher values from the range
    match = re.search(r'([\d.-]+)-([\d.-]+)', range_str)
    if match:
        lower = float(match.group(1))
        higher = float(match.group(2))
    else:
        # If no range is found, assume it's a single value
        lower = float(range_str)
        higher = lower
        
    return int(higher)


def parse_phone(phone):
    if not phone:
        return None
    return phone.replace(" ", "")


def parse_description(description):
    if not description:
        return None
    # return description.replace("<br/>", "\n")
    return description


def get_lister(lister):
    lister = delete_nulls(lister)
    lister_id = lister.get("id")
    name = lister.get("name")
    agent_id = lister.get("agentId")
    job_title = lister.get("jobTitle")
    url = lister.get("_links", {}).get("canonical", {}).get("href")
    phone = parse_phone(lister.get("preferredPhoneNumber"))
    email = lister.get("email")  # TODO untested, need to confirm
    return Lister(
        id=lister_id,
        name=name,
        agent_id=agent_id,
        job_title=job_title,
        url=url,
        phone=phone,
        email=email,
    )

def get_image(media):
    """Creates an object representing an image from the listing. Replaces the {size} parameter with a known working varaible"""
    size_to_insert_into_link = '1144x888-format=webp'
    return MediaItem(
        link=media.get('templatedUrl',{}).replace("{size}", size_to_insert_into_link)
    )

def get_listing(listing):
    listing = delete_nulls(listing)
    # delete null keys for convenience

    property_id = listing.get("id")
    badge = listing.get("badge", {}).get("label")
    url = listing.get("_links", {}).get("canonical", {}).get("href")
    address = listing.get("address", {})
    suburb = address.get("suburb")
    state = address.get("state")
    postcode = address.get("postcode")
    short_address = address.get("display", {}).get("shortAddress")
    full_address = address.get("display", {}).get("fullAddress")
    property_type = listing.get("propertyType", {}).get("id")
    listing_company = listing.get("listingCompany", {})
    listing_company_id = listing_company.get("id")
    listing_company_name = listing_company.get("name")
    listing_company_phone = parse_phone(listing_company.get("businessPhone"))
    features = listing.get("generalFeatures", {})
    bedrooms = features.get("bedrooms", {}).get("value")
    bathrooms = features.get("bathrooms", {}).get("value")
    parking_spaces = features.get("parkingSpaces", {}).get("value")
    property_sizes = listing.get("propertySizes", {})
    building_size = property_sizes.get("building", {}).get("displayValue")
    building_size_unit = property_sizes.get(
        "building", {}).get("sizeUnit", {}).get("displayValue")
    land_size = float(''.join(property_sizes.get(
        "land", {}).get("displayValue", '-1').split(',')))
    land_size_unit = property_sizes.get("land", {}).get(
        "sizeUnit", {}).get("displayValue")
    price_text = listing.get("price", {}).get("display", "")
    price = parse_price_text(price_text)
    price_text = listing.get("price", {}).get("display")
    sold_date = listing.get("dateSold", {}).get("display")
    auction = listing.get("auction", {}) or {}
    auction_date = auction.get("dateTime", {}).get("value")
    description = parse_description(listing.get("description"))
    images = [get_image(media) for media in listing.get("media", []).get('images',[])]
    images_floorplans = [get_image(media) for media in listing.get("media", []).get('floorplans',[])]
    listers = [get_lister(lister) for lister in listing.get("listers", [])]

    return Listing(
        id=property_id,
        badge=badge,
        url=url,
        suburb=suburb,
        state=state,
        postcode=postcode,
        short_address=short_address,
        full_address=full_address,
        property_type=property_type,
        listing_company_id=listing_company_id,
        listing_company_name=listing_company_name,
        listing_company_phone=listing_company_phone,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        parking_spaces=parking_spaces,
        building_size=building_size,
        building_size_unit=building_size_unit,
        land_size=land_size,
        land_size_unit=land_size_unit,
        price=price,
        price_text=price_text,
        auction_date=auction_date,
        sold_date=sold_date,
        description=description,
        images=images,
        images_floorplans=images_floorplans,
        listers=listers,
    )

if __name__ == "__main__":
    pass

    # Test the code with example values
    test_values = [
        '$4M',
        '250K',
        '500,000',
        '565-575K',
        '$1M - $1.1M',
        '$350,000 - $380,000',
        '565-575K',
        '565k to 570k',
        '$420-440K',
        '$1.55 - $1.65 Best Offers By Mon 21st Nov at 10am',
        '1050K to 1090K',
        'from $1.199.000M',
        '$209 - $239,000',
        '690,000-720,000',
        '$1.1-1.15m',
        '$1M - $1.1M'
    ]

    test_txt = '565-575K' 
    test_txt = '$1M - $1.1M' 
    test_txt = '$350,000 - $380,000'    #COMMON FORMAT !!
    test_txt = '565-575K'  
    test_txt = '120,000.00'  

    print(f'👍👍👍Testing Phrase: {test_txt}')
    x = parse_price_text(test_txt)
    print(f'✨✨✨ Output: {x}')