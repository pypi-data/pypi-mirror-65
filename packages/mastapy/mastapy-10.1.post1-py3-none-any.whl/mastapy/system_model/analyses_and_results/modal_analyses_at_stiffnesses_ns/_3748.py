'''_3748.py

ConceptGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2059
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6074
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3773
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ConceptGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearModalAnalysesAtStiffnesses',)


class ConceptGearModalAnalysesAtStiffnesses(_3773.GearModalAnalysesAtStiffnesses):
    '''ConceptGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2059.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2059.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6074.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6074.ConceptGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
