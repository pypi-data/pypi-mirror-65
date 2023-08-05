'''_5228.py

PartStaticLoadCaseGroup
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _1986, _1957, _1958, _1959,
    _1962, _1964, _1965, _1966,
    _1969, _1970, _1973, _1974,
    _1975, _1978, _1981, _1982,
    _1983, _1985, _1987, _1989,
    _1990, _1992, _1994, _1995,
    _1996
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _1999
from mastapy.system_model.part_model.gears import (
    _2029, _2030, _2031, _2032,
    _2033, _2034, _2035, _2036,
    _2037, _2038, _2039, _2040,
    _2041, _2042, _2043, _2044,
    _2045, _2046, _2048, _2050,
    _2051, _2052, _2053, _2054,
    _2055, _2056, _2057, _2058,
    _2059, _2060, _2061, _2062,
    _2063, _2064, _2065, _2066,
    _2067, _2068, _2069, _2070
)
from mastapy.system_model.part_model.couplings import (
    _2088, _2090, _2091, _2093,
    _2094, _2095, _2096, _2097,
    _2098, _2099, _2100, _2101,
    _2107, _2108, _2109, _2110,
    _2111, _2112, _2114, _2115,
    _2116, _2117, _2118, _2120
)
from mastapy.system_model.analyses_and_results.static_loads import _6132
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5226
from mastapy._internal.python_net import python_net_import

_PART_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'PartStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('PartStaticLoadCaseGroup',)


class PartStaticLoadCaseGroup(_5226.DesignEntityStaticLoadCaseGroup):
    '''PartStaticLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _PART_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clear_user_specified_excitation_data_for_all_load_cases(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearUserSpecifiedExcitationDataForAllLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearUserSpecifiedExcitationDataForAllLoadCases

    @property
    def part(self) -> '_1986.Part':
        '''Part: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.Part)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_assembly(self) -> '_1957.Assembly':
        '''Assembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.Assembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Assembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1957.Assembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_abstract_assembly(self) -> '_1958.AbstractAssembly':
        '''AbstractAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1958.AbstractAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AbstractAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1958.AbstractAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_abstract_shaft_or_housing(self) -> '_1959.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.AbstractShaftOrHousing.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1959.AbstractShaftOrHousing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bearing(self) -> '_1962.Bearing':
        '''Bearing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.Bearing.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Bearing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1962.Bearing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bolt(self) -> '_1964.Bolt':
        '''Bolt: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.Bolt.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Bolt. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1964.Bolt)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bolted_joint(self) -> '_1965.BoltedJoint':
        '''BoltedJoint: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.BoltedJoint.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BoltedJoint. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1965.BoltedJoint)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_component(self) -> '_1966.Component':
        '''Component: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1966.Component.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Component. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1966.Component)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_connector(self) -> '_1969.Connector':
        '''Connector: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.Connector.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Connector. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1969.Connector)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_datum(self) -> '_1970.Datum':
        '''Datum: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.Datum.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Datum. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1970.Datum)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_external_cad_model(self) -> '_1973.ExternalCADModel':
        '''ExternalCADModel: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.ExternalCADModel.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ExternalCADModel. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1973.ExternalCADModel)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_flexible_pin_assembly(self) -> '_1974.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.FlexiblePinAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1974.FlexiblePinAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_guide_dxf_model(self) -> '_1975.GuideDxfModel':
        '''GuideDxfModel: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.GuideDxfModel.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to GuideDxfModel. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1975.GuideDxfModel)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_imported_fe_component(self) -> '_1978.ImportedFEComponent':
        '''ImportedFEComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1978.ImportedFEComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1978.ImportedFEComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_mass_disc(self) -> '_1981.MassDisc':
        '''MassDisc: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.MassDisc.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to MassDisc. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1981.MassDisc)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_measurement_component(self) -> '_1982.MeasurementComponent':
        '''MeasurementComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.MeasurementComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to MeasurementComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1982.MeasurementComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_mountable_component(self) -> '_1983.MountableComponent':
        '''MountableComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.MountableComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to MountableComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1983.MountableComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_oil_seal(self) -> '_1985.OilSeal':
        '''OilSeal: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.OilSeal.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to OilSeal. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1985.OilSeal)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_planet_carrier(self) -> '_1987.PlanetCarrier':
        '''PlanetCarrier: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.PlanetCarrier.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PlanetCarrier. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1987.PlanetCarrier)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_point_load(self) -> '_1989.PointLoad':
        '''PointLoad: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.PointLoad.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PointLoad. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1989.PointLoad)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_power_load(self) -> '_1990.PowerLoad':
        '''PowerLoad: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.PowerLoad.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PowerLoad. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1990.PowerLoad)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_root_assembly(self) -> '_1992.RootAssembly':
        '''RootAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.RootAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to RootAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1992.RootAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_specialised_assembly(self) -> '_1994.SpecialisedAssembly':
        '''SpecialisedAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.SpecialisedAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1994.SpecialisedAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_unbalanced_mass(self) -> '_1995.UnbalancedMass':
        '''UnbalancedMass: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.UnbalancedMass.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to UnbalancedMass. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1995.UnbalancedMass)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_virtual_component(self) -> '_1996.VirtualComponent':
        '''VirtualComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.VirtualComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to VirtualComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1996.VirtualComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_shaft(self) -> '_1999.Shaft':
        '''Shaft: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.Shaft.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Shaft. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1999.Shaft)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_agma_gleason_conical_gear(self) -> '_2029.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.AGMAGleasonConicalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2029.AGMAGleasonConicalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_agma_gleason_conical_gear_set(self) -> '_2030.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2030.AGMAGleasonConicalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_gear(self) -> '_2031.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.BevelDifferentialGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2031.BevelDifferentialGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_gear_set(self) -> '_2032.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.BevelDifferentialGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2032.BevelDifferentialGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_planet_gear(self) -> '_2033.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2033.BevelDifferentialPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_sun_gear(self) -> '_2034.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.BevelDifferentialSunGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2034.BevelDifferentialSunGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_gear(self) -> '_2035.BevelGear':
        '''BevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.BevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2035.BevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_gear_set(self) -> '_2036.BevelGearSet':
        '''BevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2036.BevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2036.BevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_gear(self) -> '_2037.ConceptGear':
        '''ConceptGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.ConceptGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2037.ConceptGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_gear_set(self) -> '_2038.ConceptGearSet':
        '''ConceptGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.ConceptGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2038.ConceptGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_conical_gear(self) -> '_2039.ConicalGear':
        '''ConicalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.ConicalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConicalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2039.ConicalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_conical_gear_set(self) -> '_2040.ConicalGearSet':
        '''ConicalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.ConicalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConicalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2040.ConicalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_gear(self) -> '_2041.CylindricalGear':
        '''CylindricalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.CylindricalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CylindricalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2041.CylindricalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_gear_set(self) -> '_2042.CylindricalGearSet':
        '''CylindricalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.CylindricalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CylindricalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2042.CylindricalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_planet_gear(self) -> '_2043.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.CylindricalPlanetGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2043.CylindricalPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_face_gear(self) -> '_2044.FaceGear':
        '''FaceGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.FaceGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to FaceGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2044.FaceGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_face_gear_set(self) -> '_2045.FaceGearSet':
        '''FaceGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.FaceGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to FaceGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2045.FaceGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_gear(self) -> '_2046.Gear':
        '''Gear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.Gear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Gear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2046.Gear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_gear_set(self) -> '_2048.GearSet':
        '''GearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.GearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to GearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2048.GearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_hypoid_gear(self) -> '_2050.HypoidGear':
        '''HypoidGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.HypoidGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to HypoidGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2050.HypoidGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_hypoid_gear_set(self) -> '_2051.HypoidGearSet':
        '''HypoidGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.HypoidGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to HypoidGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2051.HypoidGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2052.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2052.KlingelnbergCycloPalloidConicalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2053.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2053.KlingelnbergCycloPalloidConicalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2054.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2054.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2055.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2055.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2056.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2056.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2057.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_planetary_gear_set(self) -> '_2058.PlanetaryGearSet':
        '''PlanetaryGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.PlanetaryGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2058.PlanetaryGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spiral_bevel_gear(self) -> '_2059.SpiralBevelGear':
        '''SpiralBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.SpiralBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2059.SpiralBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spiral_bevel_gear_set(self) -> '_2060.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.SpiralBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2060.SpiralBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_diff_gear(self) -> '_2061.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.StraightBevelDiffGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2061.StraightBevelDiffGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_diff_gear_set(self) -> '_2062.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.StraightBevelDiffGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2062.StraightBevelDiffGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_gear(self) -> '_2063.StraightBevelGear':
        '''StraightBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.StraightBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2063.StraightBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_gear_set(self) -> '_2064.StraightBevelGearSet':
        '''StraightBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.StraightBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2064.StraightBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_planet_gear(self) -> '_2065.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.StraightBevelPlanetGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2065.StraightBevelPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_sun_gear(self) -> '_2066.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.StraightBevelSunGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2066.StraightBevelSunGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_worm_gear(self) -> '_2067.WormGear':
        '''WormGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.WormGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to WormGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2067.WormGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_worm_gear_set(self) -> '_2068.WormGearSet':
        '''WormGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.WormGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to WormGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2068.WormGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_zerol_bevel_gear(self) -> '_2069.ZerolBevelGear':
        '''ZerolBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.ZerolBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2069.ZerolBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_zerol_bevel_gear_set(self) -> '_2070.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.ZerolBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2070.ZerolBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_belt_drive(self) -> '_2088.BeltDrive':
        '''BeltDrive: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.BeltDrive.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BeltDrive. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2088.BeltDrive)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_clutch(self) -> '_2090.Clutch':
        '''Clutch: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.Clutch.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Clutch. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2090.Clutch)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_clutch_half(self) -> '_2091.ClutchHalf':
        '''ClutchHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.ClutchHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ClutchHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2091.ClutchHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_coupling(self) -> '_2093.ConceptCoupling':
        '''ConceptCoupling: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2093.ConceptCoupling.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptCoupling. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2093.ConceptCoupling)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_coupling_half(self) -> '_2094.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.ConceptCouplingHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2094.ConceptCouplingHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_coupling(self) -> '_2095.Coupling':
        '''Coupling: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2095.Coupling.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Coupling. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2095.Coupling)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_coupling_half(self) -> '_2096.CouplingHalf':
        '''CouplingHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.CouplingHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CouplingHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2096.CouplingHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cvt(self) -> '_2097.CVT':
        '''CVT: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.CVT.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CVT. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2097.CVT)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cvt_pulley(self) -> '_2098.CVTPulley':
        '''CVTPulley: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.CVTPulley.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CVTPulley. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2098.CVTPulley)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_part_to_part_shear_coupling(self) -> '_2099.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.PartToPartShearCoupling.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2099.PartToPartShearCoupling)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_part_to_part_shear_coupling_half(self) -> '_2100.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2100.PartToPartShearCouplingHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_pulley(self) -> '_2101.Pulley':
        '''Pulley: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.Pulley.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Pulley. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2101.Pulley)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_rolling_ring(self) -> '_2107.RollingRing':
        '''RollingRing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2107.RollingRing.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to RollingRing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2107.RollingRing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_rolling_ring_assembly(self) -> '_2108.RollingRingAssembly':
        '''RollingRingAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2108.RollingRingAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to RollingRingAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2108.RollingRingAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_shaft_hub_connection(self) -> '_2109.ShaftHubConnection':
        '''ShaftHubConnection: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2109.ShaftHubConnection.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2109.ShaftHubConnection)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spring_damper(self) -> '_2110.SpringDamper':
        '''SpringDamper: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2110.SpringDamper.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpringDamper. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2110.SpringDamper)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spring_damper_half(self) -> '_2111.SpringDamperHalf':
        '''SpringDamperHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.SpringDamperHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2111.SpringDamperHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser(self) -> '_2112.Synchroniser':
        '''Synchroniser: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.Synchroniser.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Synchroniser. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2112.Synchroniser)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_half(self) -> '_2114.SynchroniserHalf':
        '''SynchroniserHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.SynchroniserHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2114.SynchroniserHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_part(self) -> '_2115.SynchroniserPart':
        '''SynchroniserPart: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.SynchroniserPart.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SynchroniserPart. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2115.SynchroniserPart)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_sleeve(self) -> '_2116.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2116.SynchroniserSleeve.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2116.SynchroniserSleeve)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter(self) -> '_2117.TorqueConverter':
        '''TorqueConverter: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2117.TorqueConverter.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to TorqueConverter. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2117.TorqueConverter)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter_pump(self) -> '_2118.TorqueConverterPump':
        '''TorqueConverterPump: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.TorqueConverterPump.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2118.TorqueConverterPump)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter_turbine(self) -> '_2120.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.TorqueConverterTurbine.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2120.TorqueConverterTurbine)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_load_cases(self) -> 'List[_6132.PartLoadCase]':
        '''List[PartLoadCase]: 'PartLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartLoadCases, constructor.new(_6132.PartLoadCase))
        return value
