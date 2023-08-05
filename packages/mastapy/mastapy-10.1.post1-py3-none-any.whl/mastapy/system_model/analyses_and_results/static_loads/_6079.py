'''_6079.py

ConicalGearMeshLoadCase
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import (
    _1867, _1859, _1861, _1863,
    _1875, _1878, _1879, _1880,
    _1883, _1885, _1887, _1891
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.conical import _900, _894
from mastapy.system_model.analyses_and_results.static_loads import _6119
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConicalGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshLoadCase',)


class ConicalGearMeshLoadCase(_6119.GearMeshLoadCase):
    '''ConicalGearMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def crowning(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Crowning' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Crowning) if self.wrapped.Crowning else None

    @crowning.setter
    def crowning(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Crowning = value

    @property
    def use_gleason_gems_data_for_efficiency(self) -> 'bool':
        '''bool: 'UseGleasonGEMSDataForEfficiency' is the original name of this property.'''

        return self.wrapped.UseGleasonGEMSDataForEfficiency

    @use_gleason_gems_data_for_efficiency.setter
    def use_gleason_gems_data_for_efficiency(self, value: 'bool'):
        self.wrapped.UseGleasonGEMSDataForEfficiency = bool(value) if value else False

    @property
    def use_ki_mo_s_data_for_efficiency(self) -> 'bool':
        '''bool: 'UseKIMoSDataForEfficiency' is the original name of this property.'''

        return self.wrapped.UseKIMoSDataForEfficiency

    @use_ki_mo_s_data_for_efficiency.setter
    def use_ki_mo_s_data_for_efficiency(self, value: 'bool'):
        self.wrapped.UseKIMoSDataForEfficiency = bool(value) if value else False

    @property
    def use_user_specified_misalignments_in_tca(self) -> 'bool':
        '''bool: 'UseUserSpecifiedMisalignmentsInTCA' is the original name of this property.'''

        return self.wrapped.UseUserSpecifiedMisalignmentsInTCA

    @use_user_specified_misalignments_in_tca.setter
    def use_user_specified_misalignments_in_tca(self, value: 'bool'):
        self.wrapped.UseUserSpecifiedMisalignmentsInTCA = bool(value) if value else False

    @property
    def connection_design(self) -> '_1867.ConicalGearMesh':
        '''ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1867.ConicalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1859.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1859.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1859.AGMAGleasonConicalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1861.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1861.BevelDifferentialGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1861.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_1863.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1863.BevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1863.BevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1875.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1875.HypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1875.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1878.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1878.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1878.KlingelnbergCycloPalloidConicalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1879.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1879.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1879.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1880.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1880.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1880.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1883.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1883.SpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1883.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1885.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1885.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1885.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1887.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1887.StraightBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1887.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1891.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1891.ZerolBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1891.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def results_from_imported_xml(self) -> '_900.KimosBevelHypoidSingleLoadCaseResultsData':
        '''KimosBevelHypoidSingleLoadCaseResultsData: 'ResultsFromImportedXML' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_900.KimosBevelHypoidSingleLoadCaseResultsData)(self.wrapped.ResultsFromImportedXML) if self.wrapped.ResultsFromImportedXML else None

    @property
    def user_specified_misalignments(self) -> '_894.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'UserSpecifiedMisalignments' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_894.ConicalMeshMisalignments)(self.wrapped.UserSpecifiedMisalignments) if self.wrapped.UserSpecifiedMisalignments else None
