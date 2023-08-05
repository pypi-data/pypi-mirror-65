'''_4819.py

UnbalancedMassModalAnalysis
'''


from mastapy.system_model.part_model import _2017
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6206
from mastapy.system_model.analyses_and_results.system_deflections import _2337
from mastapy.system_model.analyses_and_results.modal_analyses import _4820
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'UnbalancedMassModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassModalAnalysis',)


class UnbalancedMassModalAnalysis(_4820.VirtualComponentModalAnalysis):
    '''UnbalancedMassModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2017.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6206.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6206.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2337.UnbalancedMassSystemDeflection':
        '''UnbalancedMassSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2337.UnbalancedMassSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
