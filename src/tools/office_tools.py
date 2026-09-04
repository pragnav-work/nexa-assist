from .csv_utils import read_csv


def get_office_location(city: str) -> dict:
    """Get NexaCore office information for a city."""

    offices = read_csv("office_locations.csv")

    result = offices[
        offices["city"].astype(str).str.lower() == city.strip().lower()
    ]

    if result.empty:
        return {
            "success": False,
            "message": f"No NexaCore office found in {city}.",
        }

    return {
        "success": True,
        "office": result.iloc[0].to_dict(),
    }