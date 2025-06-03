import enum

class AssetStatus(str, enum.Enum):
    in_use = "In Use"
    under_maintenance = "Under Maintenance"
    retired = "Retired"

