import re

# Normalize vehicle registration number
def normalise_registration_number(registration_number: str) -> str:
    # Remove spaces, hyphens, slashes, and commas, and convert to lowercase
    return re.sub(r"[\s\-/,]", "", registration_number.strip().casefold())
