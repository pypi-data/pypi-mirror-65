'''_3302.py

RollingRingConnectionPowerFlow
'''


from mastapy.system_model.connections_and_sockets import _1851
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6169
from mastapy.system_model.analyses_and_results.power_flows import _3275
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RollingRingConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionPowerFlow',)


class RollingRingConnectionPowerFlow(_3275.InterMountableComponentConnectionPowerFlow):
    '''RollingRingConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1851.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1851.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6169.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6169.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
