'''_3745.py

ConceptCouplingHalfModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2116
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6072
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3756
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ConceptCouplingHalfModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfModalAnalysesAtStiffnesses',)


class ConceptCouplingHalfModalAnalysesAtStiffnesses(_3756.CouplingHalfModalAnalysesAtStiffnesses):
    '''ConceptCouplingHalfModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2116.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6072.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6072.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
