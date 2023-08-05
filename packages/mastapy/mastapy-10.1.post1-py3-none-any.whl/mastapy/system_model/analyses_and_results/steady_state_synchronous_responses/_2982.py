'''_2982.py

ClutchConnectionSteadyStateSynchronousResponse
'''


from mastapy.system_model.connections_and_sockets.couplings import _1893
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6066
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2998
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ClutchConnectionSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionSteadyStateSynchronousResponse',)


class ClutchConnectionSteadyStateSynchronousResponse(_2998.CouplingConnectionSteadyStateSynchronousResponse):
    '''ClutchConnectionSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1893.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1893.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6066.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6066.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
