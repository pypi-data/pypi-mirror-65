'''_2525.py

FaceGearSetSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2067
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6114
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2526, _2524, _2529
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'FaceGearSetSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetSteadyStateSynchronousResponseOnAShaft',)


class FaceGearSetSteadyStateSynchronousResponseOnAShaft(_2529.GearSetSteadyStateSynchronousResponseOnAShaft):
    '''FaceGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2067.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2067.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6114.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6114.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2526.FaceGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[FaceGearSteadyStateSynchronousResponseOnAShaft]: 'FaceGearsSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsSteadyStateSynchronousResponseOnAShaft, constructor.new(_2526.FaceGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def face_meshes_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2524.FaceGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[FaceGearMeshSteadyStateSynchronousResponseOnAShaft]: 'FaceMeshesSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesSteadyStateSynchronousResponseOnAShaft, constructor.new(_2524.FaceGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value
