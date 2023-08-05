'''_3274.py

ImportedFEComponentPowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2000
from mastapy.system_model.analyses_and_results.static_loads import _6135
from mastapy.system_model.analyses_and_results.power_flows import _3216
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ImportedFEComponentPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentPowerFlow',)


class ImportedFEComponentPowerFlow(_3216.AbstractShaftOrHousingPowerFlow):
    '''ImportedFEComponentPowerFlow

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def speed(self) -> 'float':
        '''float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Speed

    @property
    def fe_components_are_not_used_in_power_flow_select_component_replaced_by_this_fe(self) -> 'str':
        '''str: 'FEComponentsAreNotUsedInPowerFlowSelectComponentReplacedByThisFE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEComponentsAreNotUsedInPowerFlowSelectComponentReplacedByThisFE

    @property
    def fe_components_are_not_used_in_power_flow(self) -> 'str':
        '''str: 'FEComponentsAreNotUsedInPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEComponentsAreNotUsedInPowerFlow

    @property
    def component_design(self) -> '_2000.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2000.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6135.ImportedFEComponentLoadCase':
        '''ImportedFEComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6135.ImportedFEComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
