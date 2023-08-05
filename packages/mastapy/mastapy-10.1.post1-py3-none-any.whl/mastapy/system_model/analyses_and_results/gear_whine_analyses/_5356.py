'''_5356.py

RollingRingAssemblyGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2130
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6168
from mastapy.system_model.analyses_and_results.system_deflections import _2300
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5364
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'RollingRingAssemblyGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyGearWhineAnalysis',)


class RollingRingAssemblyGearWhineAnalysis(_5364.SpecialisedAssemblyGearWhineAnalysis):
    '''RollingRingAssemblyGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2130.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6168.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6168.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2300.RollingRingAssemblySystemDeflection':
        '''RollingRingAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2300.RollingRingAssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
