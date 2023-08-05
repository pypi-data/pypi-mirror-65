'''_3272.py

HypoidGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2072
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6132
from mastapy.gears.rating.hypoid import _242
from mastapy.system_model.analyses_and_results.power_flows import _3218
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'HypoidGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearPowerFlow',)


class HypoidGearPowerFlow(_3218.AGMAGleasonConicalGearPowerFlow):
    '''HypoidGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2072.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2072.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6132.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6132.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_242.HypoidGearRating':
        '''HypoidGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_242.HypoidGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
