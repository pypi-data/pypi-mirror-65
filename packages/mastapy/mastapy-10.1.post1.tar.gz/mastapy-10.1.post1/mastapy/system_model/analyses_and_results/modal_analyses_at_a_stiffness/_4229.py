'''_4229.py

BoltModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _1986
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4234
from mastapy._internal.python_net import python_net_import

_BOLT_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'BoltModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltModalAnalysisAtAStiffness',)


class BoltModalAnalysisAtAStiffness(_4234.ComponentModalAnalysisAtAStiffness):
    '''BoltModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BOLT_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1986.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6065.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6065.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
