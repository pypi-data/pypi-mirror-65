'''_2959.py

BoltSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _1964
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6043
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2964
from mastapy._internal.python_net import python_net_import

_BOLT_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'BoltSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltSteadyStateSynchronousResponse',)


class BoltSteadyStateSynchronousResponse(_2964.ComponentSteadyStateSynchronousResponse):
    '''BoltSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BOLT_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1964.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1964.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6043.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6043.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
