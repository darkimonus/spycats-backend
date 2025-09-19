import requests
from django.core.exceptions import ValidationError


def validate_breed(value):
    try:
        response = requests.get("https://api.thecatapi.com/v1/breeds")
        response.raise_for_status()
        breeds = [breed['name'] for breed in response.json()]

        if value not in breeds:
            raise ValidationError(f"{value} is not a valid breed. Please enter a valid breed.")
    except requests.RequestException:
        raise ValidationError("Unable to verify breed due to API connection issues.")
