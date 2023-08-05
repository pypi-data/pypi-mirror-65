'''_3804.py

PowerLoadModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model import _2012
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6165
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3837
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'PowerLoadModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadModalAnalysesAtStiffnesses',)


class PowerLoadModalAnalysesAtStiffnesses(_3837.VirtualComponentModalAnalysesAtStiffnesses):
    '''PowerLoadModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2012.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6165.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6165.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
