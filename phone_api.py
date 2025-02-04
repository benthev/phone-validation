import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("TRESTLE_API_KEY")
api_url = "https://api.trestleiq.com/3.0/phone_intel"


def validate_phone(phone_number: str, country_hint: str = "US") -> dict:
    """
    Validates a phone number using the TrestleIQ API with an optional country hint.
    Args:
        phone_number (str): The phone number to validate.
        country_hint (str): The country hint for validation (default: "US").

    Returns:
        dict: The API response.
    """
    headers = {"x-api-key": api_key}
    query = {
        "phone": phone_number,
        "phone.country_hint": country_hint
    }
    try:
        response = requests.get(api_url, headers=headers, params=query)
        response.raise_for_status()
        result = response.json()
        result["phone_number_input_api"] = phone_number
        return result
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "phone": phone_number}
