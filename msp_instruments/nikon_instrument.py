#generates an instrument for the Nikon 2P single plane ophys rig

from datetime import date

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit, SizeUnit
from aind_data_schema_models.devices import CameraTarget, DataInterface, FilterType
from aind_data_schema_models.coordinates import AnatomicalRelative

from aind_data_schema.components.coordinates import (
    CoordinateSystemLibrary,
    Affine,
    Translation,
)
from aind_data_schema.components.devices import (
    Camera,
    CameraAssembly,
    Cooling,
    DAQDevice,
    DataInterface,
    Detector,
    Disc,
    Filter,
    Laser,
    Lens,
    LightEmittingDiode,
    Microscope,
    Monitor,
    Objective,
    PockelsCell,
    Computer,
)

from aind_data_schema.components.identifiers import Software
from aind_data_schema.core.instrument import Instrument

instrument = Instrument(
    instrument_id="Nikon2P.1",
    modification_date=(2015,01,01), #TODO: what should this be
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
    notes="Created several years posthoc from incomplete records. Much information is missing.",
    temperature_control=None,
    components=[
        Microscope(
            name="Nikon",
            manufacturer=Organization.NIKON,
            model="A1R MP+",
            notes="Adapted to provide space for behavior apparatus"
        ),
        Laser(
            name="Ti Sapphire",
            manufacturer=Organization.COHERENT_SCIENTIFIC,
            model="Chameleon Ti:Sapphire",
            wavelength=910,
        ),
        Disc(
            name="MindScope Running Disc",
            serial_number=None,
            manufacturer=Organization.AIND,
            surface_material="Kittrich Magic Cover Solid Grip Liner",
            radius=8.255,
            radius_unit="centimeter",
            output="Digital Output",
            encoder="CUI Devices AMT102-V 0000 Dip Switch 2048 ppr",
            decoder="LS7366R",
            encoder_firmware=Software(
                name="ls7366r_quadrature_counter",
                version="0.1.6",
            ),
        ),
        CameraAssembly(
            name="Eye Camera Assembly",
            target=CameraTarget.EYE,
            relative_position=[AnatomicalRelative.RIGHT],
            camera=Camera(
                name="Eye Camera",
                detector_type="Camera",
                serial_number=None,
                manufacturer=Organization.ALLIED,
                model="Mako G-32B",
                notes="Assuming same camera as current setup",
                data_interface="Ethernet",
                cooling=Cooling.NO_COOLING,
                frame_rate=30.0,
                frame_rate_unit=FrequencyUnit.HZ,
                chroma="Monochrome",
            ),
            lens=Lens(
                name="Eye Camera Lens",
                manufacturer=Organization.EDMUND_OPTICS,
                model="InfiniStix",
            ),
            filter=Filter(
                name="Eye Camera Filter",
                filter_type=FilterType.BANDPASS,
                manufacturer=Organization.SEMROCK,
                model="FF01-850/10-25",
                center_wavelength=850,
            )
        ),
        LightEmittingDiode(
            name="Eye Tracking LED",
            manufacturer=Organization.AMS_OSRAM,
            model="LZ1-10R702-0000",
            wavelength=850,
        ),
        CameraAssembly(
            name="Body Camera Assembly",
            target=CameraTarget.BODY,
            relative_position=[AnatomicalRelative.LEFT, AnatomicalRelative.POSTERIOR],
            camera=Camera(
                name="Body Camera",
                detector_type="Camera",
                serial_number=None,
                manufacturer=Organization.ALLIED,
                model="Mako G-32B",
                notes="Assuming same camera as current setup",
                data_interface="Ethernet",
                cooling=Cooling.NO_COOLING,
                frame_rate=30.0,
                frame_rate_unit=FrequencyUnit.HZ,
                chroma="Monochrome",
            ),
            lens=Lens(
                name="Body Camera Lens",
                manufacturer=Organization.THORLABS,
                model="MVL8M23",
            ),
            filter=Filter(
                name="Body Camera Filter",
                filter_type=FilterType.SHORTPASS,
                manufacturer=Organization.SEMROCK,
                model="BSP01-785R-25",
                cut_off_wavelength=785,
            )
        ),
        LightEmittingDiode(
            name="Body Camera LED",
            manufacturer=Organization.AMS_OSRAM,
            model="LZ4-40R308-0000",
            wavelength=740,
        ),
        Monitor(
            name="Stimulus Monitor",
            serial_number=None,
            manufacturer=Organization.ASUS,
            model="PA248Q",
            notes="viewing distance is from screen normal to bregma. Mean luminance 50 cd/m2",
            refresh_rate=60,
            width=1920,
            height=1200,
            size_unit="pixel",
            viewing_distance=15,
            viewing_distance_unit="centimeter",
            relative_position=[AnatomicalRelative.ANTERIOR, AnatomicalRelative.RIGHT],
            contrast=30,
            brightness=50,
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            transform=[
                Affine(
                    affine_transform=[
                        [
                            -0.80914,
                            -0.58761,
                            0,
                        ],
                        [
                            -0.12391,
                            0.17063,
                            0.97751,
                        ],
                        [
                            -0.5744,
                            0.79095,
                            -0.21087,
                        ],
                    ],
                ),
                Translation(
                    translation=[
                        0.08751,
                        -0.12079,
                        0.02298,
                    ],
                ),
            ],
        ),
        DAQDevice(
            name="Sync",
            manufacturer=Organization.NATIONAL_INSTRUMENTS,
            data_interface=DataInterface.PCIE,
            model="PCI-6612",
        ),
    ],
)

if __name__ == "__main__":
    serialized = instrument.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="nikon2P1_")