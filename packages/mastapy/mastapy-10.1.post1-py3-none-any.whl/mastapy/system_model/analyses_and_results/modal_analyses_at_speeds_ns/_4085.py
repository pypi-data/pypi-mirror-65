'''_4085.py

WormGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2089
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6208
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4018
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'WormGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearModalAnalysesAtSpeeds',)


class WormGearModalAnalysesAtSpeeds(_4018.GearModalAnalysesAtSpeeds):
    '''WormGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2089.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6208.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6208.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
