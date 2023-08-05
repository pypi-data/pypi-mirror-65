'''_1812.py

ComponentConnection
'''


from typing import Callable

from PIL.Image import Image

from mastapy._internal import constructor, conversion
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
from mastapy.system_model.connections_and_sockets import _1813
from mastapy._internal.python_net import python_net_import

_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentConnection',)


class ComponentConnection(_1813.ComponentMeasurer):
    '''ComponentConnection

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def socket(self) -> 'str':
        '''str: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Socket

    @property
    def connected_components_socket(self) -> 'str':
        '''str: 'ConnectedComponentsSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectedComponentsSocket

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def assembly_view(self) -> 'Image':
        '''Image: 'AssemblyView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.AssemblyView)
        return value

    @property
    def detail_view(self) -> 'Image':
        '''Image: 'DetailView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.DetailView)
        return value

    @property
    def swap(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Swap' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Swap

    @property
    def connected_component(self) -> '_1966.Component':
        '''Component: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.Component)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_abstract_shaft_or_housing(self) -> '_1959.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.AbstractShaftOrHousing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1959.AbstractShaftOrHousing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bearing(self) -> '_1962.Bearing':
        '''Bearing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.Bearing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bearing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1962.Bearing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bolt(self) -> '_1964.Bolt':
        '''Bolt: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.Bolt.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bolt. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1964.Bolt)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_connector(self) -> '_1969.Connector':
        '''Connector: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.Connector.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Connector. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1969.Connector)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_datum(self) -> '_1970.Datum':
        '''Datum: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.Datum.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Datum. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1970.Datum)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_external_cad_model(self) -> '_1973.ExternalCADModel':
        '''ExternalCADModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.ExternalCADModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ExternalCADModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1973.ExternalCADModel)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_guide_dxf_model(self) -> '_1975.GuideDxfModel':
        '''GuideDxfModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.GuideDxfModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to GuideDxfModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1975.GuideDxfModel)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_imported_fe_component(self) -> '_1978.ImportedFEComponent':
        '''ImportedFEComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1978.ImportedFEComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1978.ImportedFEComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_mass_disc(self) -> '_1981.MassDisc':
        '''MassDisc: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.MassDisc.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MassDisc. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1981.MassDisc)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_measurement_component(self) -> '_1982.MeasurementComponent':
        '''MeasurementComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.MeasurementComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MeasurementComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1982.MeasurementComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_mountable_component(self) -> '_1983.MountableComponent':
        '''MountableComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.MountableComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MountableComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1983.MountableComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_oil_seal(self) -> '_1985.OilSeal':
        '''OilSeal: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.OilSeal.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to OilSeal. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1985.OilSeal)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_planet_carrier(self) -> '_1987.PlanetCarrier':
        '''PlanetCarrier: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.PlanetCarrier.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PlanetCarrier. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1987.PlanetCarrier)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_point_load(self) -> '_1989.PointLoad':
        '''PointLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.PointLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PointLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1989.PointLoad)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_power_load(self) -> '_1990.PowerLoad':
        '''PowerLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.PowerLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PowerLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1990.PowerLoad)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_unbalanced_mass(self) -> '_1995.UnbalancedMass':
        '''UnbalancedMass: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.UnbalancedMass.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to UnbalancedMass. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1995.UnbalancedMass)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_virtual_component(self) -> '_1996.VirtualComponent':
        '''VirtualComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.VirtualComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to VirtualComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1996.VirtualComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_shaft(self) -> '_1999.Shaft':
        '''Shaft: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.Shaft.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Shaft. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1999.Shaft)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_agma_gleason_conical_gear(self) -> '_2029.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.AGMAGleasonConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2029.AGMAGleasonConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_gear(self) -> '_2031.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.BevelDifferentialGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2031.BevelDifferentialGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_planet_gear(self) -> '_2033.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.BevelDifferentialPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2033.BevelDifferentialPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_sun_gear(self) -> '_2034.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.BevelDifferentialSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2034.BevelDifferentialSunGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_gear(self) -> '_2035.BevelGear':
        '''BevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.BevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2035.BevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_concept_gear(self) -> '_2037.ConceptGear':
        '''ConceptGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.ConceptGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2037.ConceptGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_conical_gear(self) -> '_2039.ConicalGear':
        '''ConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.ConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2039.ConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cylindrical_gear(self) -> '_2041.CylindricalGear':
        '''CylindricalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.CylindricalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2041.CylindricalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cylindrical_planet_gear(self) -> '_2043.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.CylindricalPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2043.CylindricalPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_face_gear(self) -> '_2044.FaceGear':
        '''FaceGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.FaceGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to FaceGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2044.FaceGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_gear(self) -> '_2046.Gear':
        '''Gear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.Gear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Gear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2046.Gear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_hypoid_gear(self) -> '_2050.HypoidGear':
        '''HypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.HypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to HypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2050.HypoidGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2052.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2052.KlingelnbergCycloPalloidConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2054.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2054.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2056.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2056.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_spiral_bevel_gear(self) -> '_2059.SpiralBevelGear':
        '''SpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.SpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2059.SpiralBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_diff_gear(self) -> '_2061.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.StraightBevelDiffGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2061.StraightBevelDiffGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_gear(self) -> '_2063.StraightBevelGear':
        '''StraightBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.StraightBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2063.StraightBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_planet_gear(self) -> '_2065.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.StraightBevelPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2065.StraightBevelPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_sun_gear(self) -> '_2066.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.StraightBevelSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2066.StraightBevelSunGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_worm_gear(self) -> '_2067.WormGear':
        '''WormGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.WormGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to WormGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2067.WormGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_zerol_bevel_gear(self) -> '_2069.ZerolBevelGear':
        '''ZerolBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.ZerolBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2069.ZerolBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_clutch_half(self) -> '_2091.ClutchHalf':
        '''ClutchHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.ClutchHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ClutchHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2091.ClutchHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_concept_coupling_half(self) -> '_2094.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.ConceptCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2094.ConceptCouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_coupling_half(self) -> '_2096.CouplingHalf':
        '''CouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.CouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2096.CouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cvt_pulley(self) -> '_2098.CVTPulley':
        '''CVTPulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.CVTPulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CVTPulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2098.CVTPulley)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_part_to_part_shear_coupling_half(self) -> '_2100.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2100.PartToPartShearCouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_pulley(self) -> '_2101.Pulley':
        '''Pulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.Pulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Pulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2101.Pulley)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_rolling_ring(self) -> '_2107.RollingRing':
        '''RollingRing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2107.RollingRing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to RollingRing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2107.RollingRing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_shaft_hub_connection(self) -> '_2109.ShaftHubConnection':
        '''ShaftHubConnection: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2109.ShaftHubConnection.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2109.ShaftHubConnection)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_spring_damper_half(self) -> '_2111.SpringDamperHalf':
        '''SpringDamperHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.SpringDamperHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2111.SpringDamperHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_half(self) -> '_2114.SynchroniserHalf':
        '''SynchroniserHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.SynchroniserHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2114.SynchroniserHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_part(self) -> '_2115.SynchroniserPart':
        '''SynchroniserPart: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.SynchroniserPart.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserPart. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2115.SynchroniserPart)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_sleeve(self) -> '_2116.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2116.SynchroniserSleeve.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2116.SynchroniserSleeve)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_torque_converter_pump(self) -> '_2118.TorqueConverterPump':
        '''TorqueConverterPump: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.TorqueConverterPump.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2118.TorqueConverterPump)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_torque_converter_turbine(self) -> '_2120.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.TorqueConverterTurbine.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2120.TorqueConverterTurbine)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None
