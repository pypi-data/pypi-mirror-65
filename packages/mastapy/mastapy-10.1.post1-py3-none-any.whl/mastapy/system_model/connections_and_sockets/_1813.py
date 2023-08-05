'''_1813.py

ComponentMeasurer
'''


from typing import List

from mastapy._internal import constructor
from mastapy.system_model.part_model import (
    _1966, _1959, _1962, _1964,
    _1969, _1970, _1973, _1975,
    _1978, _1981, _1982, _1983,
    _1985, _1987, _1989, _1990,
    _1995, _1996
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _1999
from mastapy.system_model.part_model.gears import (
    _2029, _2031, _2033, _2034,
    _2035, _2037, _2039, _2041,
    _2043, _2044, _2046, _2050,
    _2052, _2054, _2056, _2059,
    _2061, _2063, _2065, _2066,
    _2067, _2069
)
from mastapy.system_model.part_model.couplings import (
    _2091, _2094, _2096, _2098,
    _2100, _2101, _2107, _2109,
    _2111, _2114, _2115, _2116,
    _2118, _2120
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COMPONENT_MEASURER = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentMeasurer')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentMeasurer',)


class ComponentMeasurer(_0.APIBase):
    '''ComponentMeasurer

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_MEASURER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentMeasurer.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def offset_of_component(self) -> 'float':
        '''float: 'OffsetOfComponent' is the original name of this property.'''

        return self.wrapped.OffsetOfComponent

    @offset_of_component.setter
    def offset_of_component(self, value: 'float'):
        self.wrapped.OffsetOfComponent = float(value) if value else 0.0

    @property
    def component(self) -> '_1966.Component':
        '''Component: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.Component)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_abstract_shaft_or_housing(self) -> '_1959.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.AbstractShaftOrHousing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1959.AbstractShaftOrHousing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bearing(self) -> '_1962.Bearing':
        '''Bearing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.Bearing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bearing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1962.Bearing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bolt(self) -> '_1964.Bolt':
        '''Bolt: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.Bolt.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bolt. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1964.Bolt)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_connector(self) -> '_1969.Connector':
        '''Connector: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.Connector.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Connector. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1969.Connector)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_datum(self) -> '_1970.Datum':
        '''Datum: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.Datum.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Datum. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1970.Datum)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_external_cad_model(self) -> '_1973.ExternalCADModel':
        '''ExternalCADModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.ExternalCADModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ExternalCADModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1973.ExternalCADModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_guide_dxf_model(self) -> '_1975.GuideDxfModel':
        '''GuideDxfModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.GuideDxfModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to GuideDxfModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1975.GuideDxfModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_imported_fe_component(self) -> '_1978.ImportedFEComponent':
        '''ImportedFEComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1978.ImportedFEComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1978.ImportedFEComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_mass_disc(self) -> '_1981.MassDisc':
        '''MassDisc: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.MassDisc.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MassDisc. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1981.MassDisc)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_measurement_component(self) -> '_1982.MeasurementComponent':
        '''MeasurementComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.MeasurementComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MeasurementComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1982.MeasurementComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_mountable_component(self) -> '_1983.MountableComponent':
        '''MountableComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.MountableComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MountableComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1983.MountableComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_oil_seal(self) -> '_1985.OilSeal':
        '''OilSeal: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.OilSeal.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to OilSeal. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1985.OilSeal)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_planet_carrier(self) -> '_1987.PlanetCarrier':
        '''PlanetCarrier: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.PlanetCarrier.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PlanetCarrier. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1987.PlanetCarrier)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_point_load(self) -> '_1989.PointLoad':
        '''PointLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.PointLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PointLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1989.PointLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_power_load(self) -> '_1990.PowerLoad':
        '''PowerLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.PowerLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PowerLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1990.PowerLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_unbalanced_mass(self) -> '_1995.UnbalancedMass':
        '''UnbalancedMass: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.UnbalancedMass.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to UnbalancedMass. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1995.UnbalancedMass)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_virtual_component(self) -> '_1996.VirtualComponent':
        '''VirtualComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.VirtualComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to VirtualComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1996.VirtualComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft(self) -> '_1999.Shaft':
        '''Shaft: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.Shaft.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Shaft. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1999.Shaft)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_agma_gleason_conical_gear(self) -> '_2029.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.AGMAGleasonConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2029.AGMAGleasonConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_gear(self) -> '_2031.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.BevelDifferentialGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2031.BevelDifferentialGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_planet_gear(self) -> '_2033.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2033.BevelDifferentialPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_sun_gear(self) -> '_2034.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.BevelDifferentialSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2034.BevelDifferentialSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_gear(self) -> '_2035.BevelGear':
        '''BevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.BevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2035.BevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_gear(self) -> '_2037.ConceptGear':
        '''ConceptGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.ConceptGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2037.ConceptGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_conical_gear(self) -> '_2039.ConicalGear':
        '''ConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.ConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2039.ConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_gear(self) -> '_2041.CylindricalGear':
        '''CylindricalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.CylindricalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2041.CylindricalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_planet_gear(self) -> '_2043.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.CylindricalPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2043.CylindricalPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_face_gear(self) -> '_2044.FaceGear':
        '''FaceGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.FaceGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to FaceGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2044.FaceGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_gear(self) -> '_2046.Gear':
        '''Gear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.Gear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Gear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2046.Gear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_hypoid_gear(self) -> '_2050.HypoidGear':
        '''HypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.HypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to HypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2050.HypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2052.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2052.KlingelnbergCycloPalloidConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2054.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2054.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2056.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2056.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spiral_bevel_gear(self) -> '_2059.SpiralBevelGear':
        '''SpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.SpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2059.SpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_diff_gear(self) -> '_2061.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.StraightBevelDiffGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2061.StraightBevelDiffGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_gear(self) -> '_2063.StraightBevelGear':
        '''StraightBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.StraightBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2063.StraightBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_planet_gear(self) -> '_2065.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.StraightBevelPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2065.StraightBevelPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_sun_gear(self) -> '_2066.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.StraightBevelSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2066.StraightBevelSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_worm_gear(self) -> '_2067.WormGear':
        '''WormGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.WormGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to WormGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2067.WormGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_zerol_bevel_gear(self) -> '_2069.ZerolBevelGear':
        '''ZerolBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.ZerolBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2069.ZerolBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_clutch_half(self) -> '_2091.ClutchHalf':
        '''ClutchHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.ClutchHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ClutchHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2091.ClutchHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_coupling_half(self) -> '_2094.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.ConceptCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2094.ConceptCouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_coupling_half(self) -> '_2096.CouplingHalf':
        '''CouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.CouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2096.CouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cvt_pulley(self) -> '_2098.CVTPulley':
        '''CVTPulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.CVTPulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CVTPulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2098.CVTPulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_part_to_part_shear_coupling_half(self) -> '_2100.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2100.PartToPartShearCouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_pulley(self) -> '_2101.Pulley':
        '''Pulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.Pulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Pulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2101.Pulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_rolling_ring(self) -> '_2107.RollingRing':
        '''RollingRing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2107.RollingRing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to RollingRing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2107.RollingRing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft_hub_connection(self) -> '_2109.ShaftHubConnection':
        '''ShaftHubConnection: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2109.ShaftHubConnection.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2109.ShaftHubConnection)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spring_damper_half(self) -> '_2111.SpringDamperHalf':
        '''SpringDamperHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.SpringDamperHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2111.SpringDamperHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_half(self) -> '_2114.SynchroniserHalf':
        '''SynchroniserHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.SynchroniserHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2114.SynchroniserHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_part(self) -> '_2115.SynchroniserPart':
        '''SynchroniserPart: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.SynchroniserPart.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserPart. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2115.SynchroniserPart)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_sleeve(self) -> '_2116.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2116.SynchroniserSleeve.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2116.SynchroniserSleeve)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_pump(self) -> '_2118.TorqueConverterPump':
        '''TorqueConverterPump: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.TorqueConverterPump.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2118.TorqueConverterPump)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_turbine(self) -> '_2120.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.TorqueConverterTurbine.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2120.TorqueConverterTurbine)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
