'''_3200.py

BeltConnectionPowerFlow
'''


from mastapy.system_model.connections_and_sockets import _1810
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6032
from mastapy.system_model.analyses_and_results.power_flows import _3253
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BeltConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionPowerFlow',)


class BeltConnectionPowerFlow(_3253.InterMountableComponentConnectionPowerFlow):
    '''BeltConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1810.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1810.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6032.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6032.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
