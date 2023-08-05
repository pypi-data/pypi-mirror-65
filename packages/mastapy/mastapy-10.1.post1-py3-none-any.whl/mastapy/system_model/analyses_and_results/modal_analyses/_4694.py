'''_4694.py

BoltModalAnalysis
'''


from mastapy.system_model.part_model import _1964
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6043
from mastapy.system_model.analyses_and_results.system_deflections import _2202
from mastapy.system_model.analyses_and_results.modal_analyses import _4699
from mastapy._internal.python_net import python_net_import

_BOLT_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BoltModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltModalAnalysis',)


class BoltModalAnalysis(_4699.ComponentModalAnalysis):
    '''BoltModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1964.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1964.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6043.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6043.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2202.BoltSystemDeflection':
        '''BoltSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2202.BoltSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
