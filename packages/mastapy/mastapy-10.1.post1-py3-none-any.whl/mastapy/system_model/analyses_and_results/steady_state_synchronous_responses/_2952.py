'''_2952.py

BevelDifferentialGearSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.gears import _2031
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6034
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2957
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'BevelDifferentialGearSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSteadyStateSynchronousResponse',)


class BevelDifferentialGearSteadyStateSynchronousResponse(_2957.BevelGearSteadyStateSynchronousResponse):
    '''BevelDifferentialGearSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2031.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2031.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6034.BevelDifferentialGearLoadCase':
        '''BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6034.BevelDifferentialGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
