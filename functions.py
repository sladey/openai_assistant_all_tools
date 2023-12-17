import string
import random
import requests
import dotenv
import os

dotenv.load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

class Functions:
    def get_random_digit():
        return random.randint(0,9)
    
    get_random_digit_JSON = {
        "name": "get_random_digit",
        "description": "Get a random digit",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_random_letters(count: int, case_sensitive: bool = False):
        return ''.join(random.choices(string.ascii_letters if case_sensitive else string.ascii_uppercase, k=count))

    get_random_letters_JSON = {
        "name": "get_random_letters",
        "description": "Get a string of random letters",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of letters to return"},
                "case_sensitive": {"type": "boolean", "description": "Whether to include lower-case letters.  Default only returns upper-case letters."}
            },
            "required": ["count"]
        }
    }

    def get_property_listings(state_code: str, list_price_maximum: int = -1, list_price_minimum: int = -1, minimum_number_bathrooms: int = -1, cats_allowed: bool = False, dogs_allowed: bool = False):

        url = "https://realtor.p.rapidapi.com/properties/v3/list"

        # payload = {
        #     "limit": 10,
        #     "offset": 0,
        #     "postal_code": "90210",
        #     "status": ["for_sale", "ready_to_build"],
        #     "sort": {
        #         "direction": "desc",
        #         "field": "list_date"
        #     }
        # }
        payload = {
	        "limit": 10,
            "offset": 0,
            "baths": { "min": minimum_number_bathrooms },
            "list_price": {
                "max": list_price_maximum,
                "min": list_price_minimum
            },
            "cats": cats_allowed,
            "dogs": dogs_allowed,
            "state_code": state_code,
            "status": ["for_rent"],
            "type": ["condos", "condo_townhome_rowhome_coop", "condo_townhome", "townhomes", "duplex_triplex", "single_family", "multi_family", "apartment", "condop", "coop"],
            "sort": {
                "direction": "desc",
                "field": "list_date"
        }}
        
        if list_price_maximum == -1:
            del payload["list_price"]["max"]
        if list_price_minimum == -1:
            del payload["list_price"]["min"]
        if minimum_number_bathrooms == -1:
            del payload["baths"]
        
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "realtor.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()

    get_property_listings_JSON = {
        "name": "get_property_listings",
        "description": "Get information on properties for sale or for rent in a given state or postcode",
        "parameters": {
            "type": "object",
            "properties": {
                "state_code": {"type": "string", "description": "Code for the state where properties listings must be."},
                "list_price_maximum": {"type": "integer", "description": "Maximum list price to use in search for properties."},
                "list_price_minimum": {"type": "integer", "description": "Minimum list price to use in search for properties."},
                "cats_allowed": {"type": "boolean", "description": "If true, search for properties that allow cats."},
                "dogs_allowed": {"type": "boolean", "description": "If true, search for properties that allow dogs."},
                "minimum_number_bathrooms": {"type": "integer", "description": "Minimum number of bathrooms to use in search for properties."},
            },
            "required": ["state_code"]
        }
    }

