'''_2812.py

SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2082
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6179
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2813, _2811, _2735
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed',)


class SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed(_2735.BevelGearSetSteadyStateSynchronousResponseAtASpeed):
    '''SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2082.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2082.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6179.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6179.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def spiral_bevel_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2813.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpiralBevelGearSteadyStateSynchronousResponseAtASpeed]: 'SpiralBevelGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_2813.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spiral_bevel_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2811.SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed]: 'SpiralBevelMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_2811.SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
