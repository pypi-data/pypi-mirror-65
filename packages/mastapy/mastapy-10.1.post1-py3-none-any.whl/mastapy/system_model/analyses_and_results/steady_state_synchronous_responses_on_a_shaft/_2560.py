'''_2560.py

RollingRingAssemblySteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2130
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6168
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2567
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'RollingRingAssemblySteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblySteadyStateSynchronousResponseOnAShaft',)


class RollingRingAssemblySteadyStateSynchronousResponseOnAShaft(_2567.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft):
    '''RollingRingAssemblySteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblySteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2130.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6168.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6168.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
