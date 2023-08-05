'''_3046.py

PulleySteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2123
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6166
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2999
from mastapy._internal.python_net import python_net_import

_PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'PulleySteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleySteadyStateSynchronousResponse',)


class PulleySteadyStateSynchronousResponse(_2999.CouplingHalfSteadyStateSynchronousResponse):
    '''PulleySteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleySteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2123.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2123.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6166.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6166.PulleyLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
