'''_3031.py

KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2079
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6146
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3032, _3030, _3025
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse',)


class KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse(_3025.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2079.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2079.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6146.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6146.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_steady_state_synchronous_response(self) -> 'List[_3032.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsSteadyStateSynchronousResponse, constructor.new(_3032.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_steady_state_synchronous_response(self) -> 'List[_3030.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesSteadyStateSynchronousResponse, constructor.new(_3030.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse))
        return value
