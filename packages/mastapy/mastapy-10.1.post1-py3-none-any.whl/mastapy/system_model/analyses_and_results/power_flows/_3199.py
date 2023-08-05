'''_3199.py

BearingPowerFlow
'''


from mastapy.system_model.part_model import _1962
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6031
from mastapy.bearings.bearing_results.rolling import _1661
from mastapy.system_model.analyses_and_results.power_flows import _3227
from mastapy._internal.python_net import python_net_import

_BEARING_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BearingPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingPowerFlow',)


class BearingPowerFlow(_3227.ConnectorPowerFlow):
    '''BearingPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEARING_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1962.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1962.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6031.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6031.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def rolling_bearing_speed_results(self) -> '_1661.RollingBearingSpeedResults':
        '''RollingBearingSpeedResults: 'RollingBearingSpeedResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1661.RollingBearingSpeedResults)(self.wrapped.RollingBearingSpeedResults) if self.wrapped.RollingBearingSpeedResults else None
