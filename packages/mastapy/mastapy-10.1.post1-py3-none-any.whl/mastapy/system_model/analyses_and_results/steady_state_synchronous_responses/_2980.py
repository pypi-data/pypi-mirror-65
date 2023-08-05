'''_2980.py

BoltedJointSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6064
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3054
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'BoltedJointSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointSteadyStateSynchronousResponse',)


class BoltedJointSteadyStateSynchronousResponse(_3054.SpecialisedAssemblySteadyStateSynchronousResponse):
    '''BoltedJointSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1987.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6064.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6064.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
