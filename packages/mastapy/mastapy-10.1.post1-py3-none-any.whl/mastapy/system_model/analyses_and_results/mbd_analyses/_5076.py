'''_5076.py

SpringDamperMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2132
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6182
from mastapy.system_model.analyses_and_results.mbd_analyses import _5005
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SpringDamperMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperMultiBodyDynamicsAnalysis',)


class SpringDamperMultiBodyDynamicsAnalysis(_5005.CouplingMultiBodyDynamicsAnalysis):
    '''SpringDamperMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2132.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6182.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6182.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
