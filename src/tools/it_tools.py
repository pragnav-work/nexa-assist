from .csv_utils import read_csv


def get_assigned_assets(employee_id: str) -> dict:
    """Get IT assets assigned to an employee."""

    assets = read_csv("it_assets.csv")

    result = assets[
        assets["employee_id"].astype(str).str.upper() == employee_id.upper()
    ]

    return {
        "success": True,
        "assets": result.to_dict(orient="records"),
    }