'''_4535.py

PlanetCarrierModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _2009
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6161
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4527
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'PlanetCarrierModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierModalAnalysisAtASpeed',)


class PlanetCarrierModalAnalysisAtASpeed(_4527.MountableComponentModalAnalysisAtASpeed):
    '''PlanetCarrierModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2009.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6161.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6161.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
