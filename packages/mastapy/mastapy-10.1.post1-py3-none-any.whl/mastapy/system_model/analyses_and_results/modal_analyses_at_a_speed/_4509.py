'''_4509.py

GuideDxfModelModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _1997
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6123
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4478
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'GuideDxfModelModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelModalAnalysisAtASpeed',)


class GuideDxfModelModalAnalysisAtASpeed(_4478.ComponentModalAnalysisAtASpeed):
    '''GuideDxfModelModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1997.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6123.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6123.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
