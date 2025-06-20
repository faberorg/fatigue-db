from app.database.base import Base # Import Base from app.database
from app.models.fatigue import MaterialStandardName, MaterialCategory, MaterialSubCategory, MaterialParameterName, MaterialParameter, ChemicalComposition, ChemicalElement, AlloyContent, Microstructure, MaterialDescription

# All models imported here will be available for Alembic's autogeneration.
__all__ = [
    "Base",
    "MaterialStandardName",
    "MaterialCategory",
    "MaterialSubCategory",
    "MaterialParameterName",
    "MaterialParameter",
    "ChemicalComposition",
    "ChemicalElement",
    "AlloyContent",
    "Microstructure",
    "MaterialDescription"
]
