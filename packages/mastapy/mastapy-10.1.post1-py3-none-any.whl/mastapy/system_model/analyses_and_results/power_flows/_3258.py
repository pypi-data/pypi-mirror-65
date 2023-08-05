'''_3258.py

CylindricalGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2063
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6090
from mastapy.gears.rating.cylindrical import _260
from mastapy.system_model.analyses_and_results.power_flows import _3268
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CylindricalGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearPowerFlow',)


class CylindricalGearPowerFlow(_3268.GearPowerFlow):
    '''CylindricalGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2063.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2063.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6090.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6090.CylindricalGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_260.CylindricalGearRating':
        '''CylindricalGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_260.CylindricalGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
