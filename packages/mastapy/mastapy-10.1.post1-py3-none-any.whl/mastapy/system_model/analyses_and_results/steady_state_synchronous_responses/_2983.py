'''_2983.py

ClutchHalfSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2113
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6067
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2999
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ClutchHalfSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfSteadyStateSynchronousResponse',)


class ClutchHalfSteadyStateSynchronousResponse(_2999.CouplingHalfSteadyStateSynchronousResponse):
    '''ClutchHalfSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2113.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2113.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6067.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6067.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
