'''_3336.py

WormGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2090
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6210
from mastapy.gears.rating.worm import _179
from mastapy.system_model.analyses_and_results.power_flows import _3335, _3334, _3269
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'WormGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetPowerFlow',)


class WormGearSetPowerFlow(_3269.GearSetPowerFlow):
    '''WormGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2090.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6210.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6210.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_179.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_179.WormGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_179.WormGearSetRating':
        '''WormGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_179.WormGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3335.WormGearPowerFlow]':
        '''List[WormGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3335.WormGearPowerFlow))
        return value

    @property
    def worm_gears_power_flow(self) -> 'List[_3335.WormGearPowerFlow]':
        '''List[WormGearPowerFlow]: 'WormGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsPowerFlow, constructor.new(_3335.WormGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3334.WormGearMeshPowerFlow]':
        '''List[WormGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3334.WormGearMeshPowerFlow))
        return value

    @property
    def worm_meshes_power_flow(self) -> 'List[_3334.WormGearMeshPowerFlow]':
        '''List[WormGearMeshPowerFlow]: 'WormMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesPowerFlow, constructor.new(_3334.WormGearMeshPowerFlow))
        return value
