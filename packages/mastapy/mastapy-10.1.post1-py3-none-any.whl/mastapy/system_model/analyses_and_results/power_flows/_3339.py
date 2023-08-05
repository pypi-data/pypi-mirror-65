'''_3339.py

ZerolBevelGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2092
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6213
from mastapy.gears.rating.zerol_bevel import _174
from mastapy.system_model.analyses_and_results.power_flows import _3338, _3337, _3231
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ZerolBevelGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetPowerFlow',)


class ZerolBevelGearSetPowerFlow(_3231.BevelGearSetPowerFlow):
    '''ZerolBevelGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2092.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2092.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6213.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6213.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_174.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.ZerolBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_174.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.ZerolBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3338.ZerolBevelGearPowerFlow]':
        '''List[ZerolBevelGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3338.ZerolBevelGearPowerFlow))
        return value

    @property
    def zerol_bevel_gears_power_flow(self) -> 'List[_3338.ZerolBevelGearPowerFlow]':
        '''List[ZerolBevelGearPowerFlow]: 'ZerolBevelGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsPowerFlow, constructor.new(_3338.ZerolBevelGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3337.ZerolBevelGearMeshPowerFlow]':
        '''List[ZerolBevelGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3337.ZerolBevelGearMeshPowerFlow))
        return value

    @property
    def zerol_bevel_meshes_power_flow(self) -> 'List[_3337.ZerolBevelGearMeshPowerFlow]':
        '''List[ZerolBevelGearMeshPowerFlow]: 'ZerolBevelMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesPowerFlow, constructor.new(_3337.ZerolBevelGearMeshPowerFlow))
        return value
