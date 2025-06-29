from enum import Enum


class DepartmentEnum(str, Enum):
    """
    Enum representing different functional areas of city government departments
    """

    PUBLIC_SAFETY = "Public Safety"
    TRANSPORTATION = "Transportation"
    PARKS_RECREATION = "Parks & Recreation"
    ENVIRONMENTAL = "Environmental Services"
    HEALTH_HUMAN = "Health & Human Services"
    PLANNING_DEVELOPMENT = "Planning & Development"
    EDUCATION = "Education"
    ADMINISTRATIVE = "Administrative Services"
    HOUSING = "Housing & Community Development"
    ECONOMIC_DEVELOPMENT = "Economic Development"
    UTILITIES = "Public Utilities"
    CULTURAL_AFFAIRS = "Cultural Affairs"
    ANIMAL_SERVICES = "Animal Services"
    DISABILITY_SERVICES = "Disability Services"
    TECHNOLOGY = "Technology & Innovation"

    @classmethod
    def to_dict(cls):
        return {member.name: member.value for member in cls}
