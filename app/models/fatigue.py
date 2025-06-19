from enum import StrEnum

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.meta import MetaModel


class MaterialStandardName(MetaModel):
    __tablename__ = "material_standard_names"

    # Using Mapped and mapped_column
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Foreign keys

    # Relationships
    material_descriptions: Mapped[list["MaterialDescription"]] = relationship(
        "MaterialDescription", back_populates="material_standard_name", cascade="all, delete-orphan"
    )


class MaterialCategory(MetaModel):
    __tablename__ = "material_categories"

    # Using Mapped and mapped_column
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Foreign keys

    # Relationships
    material_descriptions: Mapped[list["MaterialDescription"]] = relationship(
        "MaterialDescription", back_populates="material_category", cascade="all, delete-orphan"
    )
    material_subcategories: Mapped[list["MaterialSubCategory"]] = relationship(
        "MaterialSubCategory", back_populates="material_category", cascade="all, delete-orphan"
    )


class MaterialSubCategory(MetaModel):
    __tablename__ = "material_subcategories"

    # Using Mapped and mapped_column
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    material_category_id: Mapped[int] = mapped_column(ForeignKey("material_categories.id"), nullable=False)

    # Foreign keys

    # Relationships
    material_category: Mapped[MaterialCategory] = relationship("MaterialCategory", back_populates="material_subcategories")

    material_descriptions: Mapped[list["MaterialDescription"]] = relationship(
        "MaterialDescription", back_populates="material_subcategory", cascade="all, delete-orphan"
    )




class MaterialParameterName(MetaModel):
    __tablename__ = "material_parameter_names"

    # Using Mapped and mapped_column
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # e.g., "Density", "Young's Modulus"
    unit: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "kg/m^3", "GPa"

    # Foreign keys

    # Relationships
    material_parameters: Mapped[list["MaterialParameter"]] = relationship(
        "MaterialParameter", back_populates="material_parameter_name", cascade="all, delete-orphan"
    )


class MaterialParameter(MetaModel):
    __tablename__ = "material_parameters"

    # Using Mapped and mapped_column
    value: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "1000 kg/m^3"
    commentary: Mapped[str] = mapped_column(String, nullable=True)  # Optional comment about the parameter

    # Foreign keys
    material_description_id: Mapped[int] = mapped_column(ForeignKey("material_descriptions.id"), nullable=False)
    material_parameter_name_id: Mapped[int] = mapped_column(ForeignKey("material_parameter_names.id"), nullable=False)

    # Relationships
    material_description: Mapped["MaterialDescription"] = relationship("MaterialDescription", back_populates="material_parameters")
    material_parameter_name: Mapped["MaterialParameterName"] = relationship("MaterialParameterName", back_populates="material_parameters")


class ChemicalComposition(MetaModel):
    __tablename__ = "chemical_compositions"

    # Using Mapped and mapped_column
    source: Mapped[str] = mapped_column(String, nullable=False)  # Who provided the composition, e.g., "Manufacturer", "Standard"

    material_description_id: Mapped[int] = mapped_column(ForeignKey("material_descriptions.id"), nullable=True)  # Optional, can be null if not applicable

    # Foreign keys

    # Relationships
    alloy_contents: Mapped[list["AlloyContent"]] = relationship(
        "AlloyContent", back_populates="chemical_composition", cascade="all, delete-orphan"
    )
    material_description: Mapped["MaterialDescription"] = relationship(
        "MaterialDescription", back_populates="chemical_compositions", cascade="all, delete-orphan"
    )


class ChemicalElement(MetaModel):
    __tablename__ = "chemical_elements"

    # Using Mapped and mapped_column
    symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # e.g., "Fe", "Al"
    name: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Iron", "Aluminum"

    # Foreign keys

    # Relationships
    alloy_contents: Mapped[list["AlloyContent"]] = relationship(
        "AlloyContent", back_populates="chemical_element", cascade="all, delete-orphan"
    )


class AlloyContent(MetaModel):
    __tablename__ = "alloy_content"

    # Using Mapped and mapped_column
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # e.g., "Stainless Steel", "Bronze"
    percentage: Mapped[float] = mapped_column(nullable=False)  # Weight Percentage of the element in the alloy

    # Foreign keys
    chemical_composition_id: Mapped[int] = mapped_column(ForeignKey("chemical_compositions.id"), nullable=False)
    chemical_element_id: Mapped[int] = mapped_column(ForeignKey("chemical_elements.id"), nullable=False)

    # Relationships
    chemical_composition: Mapped["ChemicalComposition"] = relationship("ChemicalComposition", back_populates="alloy_contents")
    chemical_element: Mapped["ChemicalElement"] = relationship("ChemicalElement", back_populates="alloy_contents")


class Microstructure(MetaModel):
    __tablename__ = "microstructures"

    # Using Mapped and mapped_column
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # e.g., "Ferritic", "Austenitic"
    grain_size: Mapped[float] = mapped_column(nullable=False)  # grain size in micrometers
    crystal_structure: Mapped[str] = mapped_column(String, nullable=False)  # crystal structure description
    dislocation_density: Mapped[float] = mapped_column(nullable=False)  # dislocation density in m^-2

    image_file: Mapped[str] = mapped_column(String, nullable=True)  # e.g., microstructure photo  # TODO FILE: Add a file field

    # Foreign keys
    material_description_id: Mapped[int] = mapped_column(ForeignKey("material_descriptions.id"), nullable=True)  # Optional, can be null if not applicable

    # Relationships
    material_description: Mapped["MaterialDescription"] = relationship(
        "MaterialDescription", back_populates="microstructure", cascade="all, delete-orphan"
    )


class MaterialDescription(MetaModel):
    __tablename__ = "material_descriptions"

    # Using Mapped and mapped_column
    name: Mapped[str]
    group: Mapped[str] = mapped_column(String, nullable=True)  # e.g., "Metals", "Polymers"

    # Foreign keys
    material_standard_name_id: Mapped[int] = mapped_column(ForeignKey("material_standard_names.id"), nullable=False)
    material_category_id: Mapped[int] = mapped_column(ForeignKey("material_categories.id"), nullable=False)
    material_subcategory_id: Mapped[int] = mapped_column(ForeignKey("material_subcategories.id"), nullable=False)

    # Relationships
    material_standard_name: Mapped["MaterialStandardName"] = relationship("MaterialStandardName",
                                                                        back_populates="material_descriptions")
    material_category: Mapped["MaterialCategory"] = relationship("MaterialCategory",
                                                               back_populates="material_descriptions")
    material_subcategory: Mapped["MaterialSubCategory"] = relationship("MaterialSubCategory",
                                                                     back_populates="material_descriptions")

    chemical_compositions: Mapped[list["ChemicalComposition"]] = relationship(
        "ChemicalComposition", back_populates="material_descriptions", cascade="all, delete-orphan"
    )

    material_parameters: Mapped[list["MaterialParameter"]] = relationship(
        "MaterialParameter", back_populates="material_description", cascade="all, delete-orphan"
    )

    microstructure: Mapped["Microstructure"] = relationship("Microstructure", back_populates="material_description", cascade="all, delete-orphan")
    semi_product: Mapped["SemiProduct"] = relationship("SemiProduct", back_populates="material_description", cascade="all, delete-orphan")


class Medium(MetaModel):
    __tablename__ = "mediums"

    # Using Mapped and mapped_column
    description: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Air", "Water", "Oil"
    param_medium_meaning: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Density", "Viscosity"

    # Foreign keys

    # Relationships
    treatment: Mapped["Treatment"] = relationship(
        "Treatment", back_populates="mediums", cascade="all, delete-orphan"
    )

class Environment(MetaModel):
    __tablename__ = "environments"

    # Using Mapped and mapped_column
    description: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Atmospheric", "Vacuum", "Corrosive"
    param_environment_meaning: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Temperature", "Humidity"

    # Foreign keys

    # Relationships
    treatment: Mapped["Treatment"] = relationship(
        "Treatment", back_populates="environments", cascade="all, delete-orphan"
    )

class TreatmentProcess(MetaModel):
    __tablename__ = "treatment_processes"

    # Using Mapped and mapped_column
    treatment_process_type: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Heat Treatment", "Surface Treatment"
    param1_meaning: Mapped[str] = mapped_column(String, nullable=True)  # e.g., "Heating Temperature"
    param2_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param3_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param4_meaning: Mapped[str] = mapped_column(String, nullable=True)

    # Foreign keys

    # Relationships
    treatment: Mapped["Treatment"] = relationship(
        "Treatment", back_populates="treatment_process", cascade="all, delete-orphan"
    )


class Treatment(MetaModel):
    __tablename__ = "treatments"

    # Using Mapped and mapped_column
    order_number: Mapped[int] = mapped_column(nullable=False)  # Order of the treatment in the process
    param1: Mapped[float] = mapped_column(nullable=True)  # e.g., Temperature in °C
    param2: Mapped[float] = mapped_column(nullable=True)
    param3: Mapped[float] = mapped_column(nullable=True)
    param4: Mapped[float] = mapped_column(nullable=True)
    param_environment: Mapped[float] = mapped_column(nullable=True)  # e.g., Humidity in %
    param_medium: Mapped[float] = mapped_column(nullable=True)  # e.g., Density in kg/m^3

    # Foreign keys
    semi_product_id: Mapped[int] = mapped_column(ForeignKey("semi_products.id"), nullable=False)
    treatment_process_id: Mapped[int] = mapped_column(ForeignKey("treatment_processes.id"), nullable=False)
    environment_id: Mapped[int] = mapped_column(ForeignKey("environments.id"), nullable=False)
    medium_id: Mapped[int] = mapped_column(ForeignKey("mediums.id"), nullable=False)

    # Relationships
    semi_product: Mapped["SemiProduct"] = relationship("SemiProduct", back_populates="treatments")
    treatment_process: Mapped["TreatmentProcess"] = relationship("TreatmentProcess", back_populates="treatments")
    environment: Mapped["Environment"] = relationship("Environment", back_populates="treatments")
    medium: Mapped["Medium"] = relationship("Medium", back_populates="treatments")


class HardnessType(MetaModel):
    __tablename__ = "hardness_types"

    # Using Mapped and mapped_column
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # e.g., "Brinell", "Rockwell", "Vickers"  # TODO

    # Foreign keys

    # Relationships
    hardness: Mapped[list["Hardness"]] = relationship(
        "Hardness", back_populates="hardness_type", cascade="all, delete-orphan"
    )


class Hardness(MetaModel):
    __tablename__ = "hardness"

    # Using Mapped and mapped_column
    position: Mapped[str] = mapped_column(String, nullable=True)  # Position of the measurement on the semi-product, e.g., "Surface", "Core"
    value: Mapped[float] = mapped_column(nullable=False)  # Hardness value, e.g., 200 HB

    # Foreign keys
    semi_product_id: Mapped[int] = mapped_column(ForeignKey("semi_products.id"), nullable=False)
    hardness_type_id: Mapped[int] = mapped_column(ForeignKey("hardness_types.id"), nullable=False)

    # Relationships
    semi_product: Mapped["SemiProduct"] = relationship("SemiProduct", back_populates="hardness")
    hardness_type: Mapped["HardnessType"] = relationship("HardnessType", back_populates="hardness")


class Shape(MetaModel):
    __tablename__ = "shapes"

    # Using Mapped and mapped_column
    shape_type: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Beam", "Plate", "Cylinder"
    dimension1_meaning: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Length", "Width", "Diameter"
    dimension2_meaning: Mapped[str] = mapped_column(String, nullable=True)
    dimension3_meaning: Mapped[str] = mapped_column(String, nullable=True)
    dimension4_meaning: Mapped[str] = mapped_column(String, nullable=True)
    drawing_file: Mapped[str] = mapped_column(String, nullable=True)  # e.g., CAD files  # TODO FILE: Add a file field

    # Foreign keys

    # Relationships
    semi_product: Mapped["SemiProduct"] = relationship(
        "SemiProduct", back_populates="shape", cascade="all, delete-orphan"
    )

class SemiProduct(MetaModel):
    __tablename__ = "semi_products"

    # Using Mapped and mapped_column
    dimension1: Mapped[float] = mapped_column(nullable=False)  # e.g., Length in mm
    dimension2: Mapped[float] = mapped_column(nullable=True)
    dimension3: Mapped[float] = mapped_column(nullable=True)
    dimension4: Mapped[float] = mapped_column(nullable=True)

    # Foreign keys
    material_description_id: Mapped[int] = mapped_column(ForeignKey("material_descriptions.id"), nullable=False)
    shape_id: Mapped[int] = mapped_column(ForeignKey("shapes.id"), nullable=False)

    # Relationships
    hardness: Mapped[list["Hardness"]] = relationship("Hardness", back_populates="semi_product", cascade="all, delete-orphan")
    treatments: Mapped[list["Treatment"]] = relationship("Treatment", back_populates="semi_products", cascade="all, delete-orphan")
    material_description: Mapped["MaterialDescription"] = relationship("MaterialDescription", back_populates="semi_products")
    shape: Mapped["Shape"] = relationship("Shape", back_populates="semi_products")


class SpecimenType(MetaModel):
    __tablename__ = "specimen_types"

    # Using Mapped and mapped_column
    param1_meaning: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Length", "Diameter"
    param2_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param3_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param4_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param5_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param6_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param7_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param8_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param9_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param10_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param11_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param12_meaning: Mapped[str] = mapped_column(String, nullable=True)

    drawing_file: Mapped[str] = mapped_column(String, nullable=True)  # e.g., Drawing file for the specimen # TODO FILE: Add a file field

    # Foreign keys

    # Relationships
    specimens: Mapped[list["Specimen"]] = relationship(
        "Specimen", back_populates="specimen_type", cascade="all, delete-orphan"
    )

class SpecimenLocation(MetaModel):
    __tablename__ = "specimen_locations"

    class LocationEnum(StrEnum):  # TODO Redefine this
        SURFACE = "Surface"
        CORE = "Core"
        INTERIOR = "Interior"
        EXTERIOR = "Exterior"

    # Using Mapped and mapped_column
    location: Mapped[LocationEnum] = mapped_column(String, nullable=False)  # e.g., "Surface", "Core", "Interior", "Exterior"

    # Foreign keys

    # Relationships
    specimen: Mapped["Specimen"] = relationship(
        "Specimen", back_populates="specimen_location", cascade="all, delete-orphan"
    )


class SpecimenOrientation(MetaModel):
    __tablename__ = "specimen_orientations"

    class OrientationEnum(StrEnum):  # TODO Redefine this
        HORIZONTAL = "Horizontal"
        VERTICAL = "Vertical"
        INCLINED = "Inclined"
        RANDOM = "Random"

    # Using Mapped and mapped_column
    orientation: Mapped[OrientationEnum] = mapped_column(String, nullable=False)  # e.g., "Horizontal", "Vertical", "Inclined", "Random"

    # Foreign keys

    # Relationships
    specimen: Mapped["Specimen"] = relationship(
        "Specimen", back_populates="specimen_orientation", cascade="all, delete-orphan"
    )


class StressConcentrationFactor(MetaModel):
    __tablename__ = "stress_concentration_factors"

    class SCFEnum(StrEnum):  # TODO Redefine this
        NOTCH = "Notch"
        HOLE = "Hole"
        CORNER = "Corner"
        THREAD = "Thread"
        FILLET = "Fillet"

    # Using Mapped and mapped_column
    scf: Mapped[SCFEnum] = mapped_column(String, nullable=False)  # e.g., "Notch", "Hole", "Corner", "Thread", "Fillet"
    value: Mapped[float] = mapped_column(nullable=False)  # Stress concentration factor value, e.g., 2.0
    origin: Mapped[str] = mapped_column(String, nullable=True)  # Origin of the SCF value, e.g., "Calculated", "Measured"

    # Foreign keys
    specimen_id: Mapped[int] = mapped_column(ForeignKey("specimens.id"), nullable=False)

    # Relationships
    specimen: Mapped["Specimen"] = relationship("Specimen", back_populates="stress_concentration_factors")


class Specimen(MetaModel):
    __tablename__ = "specimens"

    # Using Mapped and mapped_column
    position: Mapped[str] = mapped_column(String, nullable=False)  # Position of the specimen, e.g., "Surface", "Core"

    param1: Mapped[float] = mapped_column(nullable=False)  # e.g., Length in mm
    param2: Mapped[float] = mapped_column(nullable=True)
    param3: Mapped[float] = mapped_column(nullable=True)
    param4: Mapped[float] = mapped_column(nullable=True)
    param5: Mapped[float] = mapped_column(nullable=True)
    param6: Mapped[float] = mapped_column(nullable=True)
    param7: Mapped[float] = mapped_column(nullable=True)
    param8: Mapped[float] = mapped_column(nullable=True)
    param9: Mapped[float] = mapped_column(nullable=True)
    param10: Mapped[float] = mapped_column(nullable=True)
    param11: Mapped[float] = mapped_column(nullable=True)
    param12: Mapped[float] = mapped_column(nullable=True)

    layout_file: Mapped[str] = mapped_column(String, nullable=True)  # e.g., Layout file for the specimen # TODO FILE: Add a file field
    drawing_file: Mapped[str] = mapped_column(String, nullable=True)  # e.g., Drawing file for the specimen # TODO FILE: Add a file field

    # Foreign keys
    specimen_type_id: Mapped[int] = mapped_column(ForeignKey("specimen_types.id"), nullable=False)
    specimen_orientation_id: Mapped[int] = mapped_column(ForeignKey("specimen_orientations.id"), nullable=False)
    specimen_location_id: Mapped[int] = mapped_column(ForeignKey("specimen_locations.id"), nullable=False)

    # Relationships
    specimen_instances: Mapped[list["SpecimenInstance"]] = relationship(
        "SpecimenInstance", back_populates="specimen", cascade="all, delete-orphan"
    )
    specimen_type: Mapped["SpecimenType"] = relationship(
        "SpecimenType", back_populates="specimens", cascade="all, delete-orphan"
    )
    specimen_orientation: Mapped["SpecimenOrientation"] = relationship(
        "SpecimenOrientation", back_populates="specimen", cascade="all, delete-orphan"
    )
    specimen_location: Mapped["SpecimenLocation"] = relationship(
        "SpecimenLocation", back_populates="specimen", cascade="all, delete-orphan"
    )
    stress_concentration_factors: Mapped[list["StressConcentrationFactor"]] = relationship(
        "StressConcentrationFactor", back_populates="specimen", cascade="all, delete-orphan"
    )


class SurfaceRoughnessType(MetaModel):
    __tablename__ = "surface_roughness_types"

    # Using Mapped and mapped_column
    # TODO

    # Foreign keys

    # Relationships
    surface_roughness: Mapped[list["SurfaceRoughness"]] = relationship(
        "SurfaceRoughness", back_populates="surface_roughness_type", cascade="all, delete-orphan"
    )


class SurfaceRoughness(MetaModel):
    __tablename__ = "surface_roughness"

    # Using Mapped and mapped_column
    value: Mapped[float] = mapped_column(nullable=False)  # Surface roughness value, e.g., 0.1 micrometers

    # Foreign keys
    specimen_id: Mapped[int] = mapped_column(ForeignKey("specimens.id"), nullable=False)
    surface_roughness_type_id: Mapped[int] = mapped_column(ForeignKey("surface_roughness_types.id"), nullable=False)

    # Relationships
    specimen: Mapped["Specimen"] = relationship("Specimen", back_populates="surface_roughness")
    surface_roughness_type: Mapped["SurfaceRoughnessType"] = relationship("RoughnessType", back_populates="surface_roughness")


class SpecimenInstance(MetaModel):
    __tablename__ = "specimen_instances"

    # Using Mapped and mapped_column
    instance_number: Mapped[int] = mapped_column(nullable=False)  # e.g., Instance number of the specimen
    # TODO

    # Foreign keys
    specimen_id: Mapped[int] = mapped_column(ForeignKey("specimens.id"), nullable=False)

    # Relationships
    specimen: Mapped["Specimen"] = relationship("Specimen", back_populates="specimen_instances")
    specimen_fatigue_test: Mapped["SpecimenFatigueTest"] = relationship(
        "SpecimenFatigueTest", back_populates="specimen_instance", cascade="all, delete-orphan"
    )
    surface_roughness: Mapped[list["SurfaceRoughness"]] = relationship(
        "SurfaceRoughness", back_populates="specimen", cascade="all, delete-orphan"
    )


class SpecimenFatigueTest(MetaModel):
    __tablename__ = "specimen_fatigue_tests"

    # Using Mapped and mapped_column
    stress_level: Mapped[float] = mapped_column(nullable=False)  # Stress level applied during the test, e.g., 100 MPa
    number_of_cycles_at_end_of_test: Mapped[int] = mapped_column(nullable=False)  # Number of cycles at the end of the test, e.g., 1000000
    number_of_cycles_at_break: Mapped[int] = mapped_column(nullable=False)  # Number of cycles to failure, e.g., 500000
    is_run_out: Mapped[bool] = mapped_column(nullable=False, default=False)  # Whether the test was a run-out (no failure)
    is_valid: Mapped[bool] = mapped_column(nullable=False, default=True)  # Whether the test is valid
    commentary: Mapped[str] = mapped_column(String, nullable=True)  # Optional commentary about the test

    # TODO list of files related to the test, e.g., test reports, raw data files
    visuals: Mapped[str] = mapped_column(String, nullable=True)  # Optional visuals related to the test, e.g., images or videos

    # Foreign keys
    specimen_instance_id: Mapped[int] = mapped_column(ForeignKey("specimen_instances.id"), nullable=False)
    fatigue_test_id: Mapped[int] = mapped_column(ForeignKey("fatigue_tests.id"), nullable=False)

    # Relationships
    specimen_instance: Mapped["SpecimenInstance"] = relationship("SpecimenInstance", back_populates="specimen_fatigue_tests")
    fatigue_test: Mapped["FatigueTest"] = relationship("FatigueTest", back_populates="specimen_fatigue_tests")


# class TestDescription(MetaModel): # TODO obsolete
#     __tablename__ = "test_descriptions"
#
#     # Using Mapped and mapped_column
#     description: Mapped[str] = mapped_column(String, nullable=True)  # Optional description of the test


class FatigueTest(MetaModel):
    __tablename__ = "fatigue_tests"

    # Using Mapped and mapped_column
    description: Mapped[str] = mapped_column(String, nullable=False)  # Description of the fatigue test, e.g., "High Cycle Fatigue Test"
    # TODO other fields

    # Foreign keys

    # Relationships
    specimen_fatigue_tests: Mapped[list["SpecimenFatigueTest"]] = relationship(
        "SpecimenFatigueTest", back_populates="fatigue_test", cascade="all, delete-orphan"
    )
    loads: Mapped[list["Load"]] = relationship(
        "Load", back_populates="fatigue_test", cascade="all, delete-orphan"
    )

class LoadMode(MetaModel):
    __tablename__ = "load_modes"

    # Using Mapped and mapped_column
    param1_meaning: Mapped[str] = mapped_column(String, nullable=False)
    param2_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param3_meaning: Mapped[str] = mapped_column(String, nullable=True)

    # Foreign keys

    # Relationships
    loads: Mapped[list["Load"]] = relationship(
        "Load", back_populates="load_mode", cascade="all, delete-orphan"
    )


class LoadSignal(MetaModel):
    __tablename__ = "load_signals"

    # Using Mapped and mapped_column
    param1_meaning: Mapped[str] = mapped_column(String, nullable=False)
    param2_meaning: Mapped[str] = mapped_column(String, nullable=True)
    param3_meaning: Mapped[str] = mapped_column(String, nullable=True)

    # Foreign keys

    # Relationships
    loads: Mapped[list["Load"]] = relationship(
        "Load", back_populates="load_signal", cascade="all, delete-orphan"
    )

class Load(MetaModel):
    __tablename__ = "loads"

    # Using Mapped and mapped_column
    order_number: Mapped[int] = mapped_column(nullable=False)  # Order of the load in the fatigue test, e.g., 1, 2, 3
    repetitions_count: Mapped[int] = mapped_column(nullable=False)  # Number of repetitions for the load, e.g., 1000
    failure: Mapped[bool] = mapped_column(nullable=False, default=False)  # Whether the load caused a failure

    param1_signal: Mapped[float] = mapped_column(nullable=False)  # e.g., Load amplitude in MPa
    param2_signal: Mapped[float] = mapped_column(nullable=True)
    param3_signal: Mapped[float] = mapped_column(nullable=True)

    param1_mode: Mapped[float] = mapped_column(nullable=True)  # e.g., Load mean in MPa
    param2_mode: Mapped[float] = mapped_column(nullable=True)
    param3_mode: Mapped[float] = mapped_column(nullable=True)


    # Foreign keys
    fatigue_test_id: Mapped[int] = mapped_column(ForeignKey("fatigue_tests.id"), nullable=False)
    load_mode_id: Mapped[int] = mapped_column(ForeignKey("load_modes.id"), nullable=False)
    load_signal_id: Mapped[int] = mapped_column(ForeignKey("load_signals.id"), nullable=False)

    # Relationships
    fatigue_test: Mapped["FatigueTest"] = relationship(
        "FatigueTest", back_populates="loads", cascade="all, delete-orphan"
    )
    load_mode: Mapped["LoadMode"] = relationship(
        "LoadMode", back_populates="loads", cascade="all, delete-orphan"
    )
    load_signal: Mapped["LoadSignal"] = relationship(
        "LoadSignal", back_populates="loads", cascade="all, delete-orphan"
    )
