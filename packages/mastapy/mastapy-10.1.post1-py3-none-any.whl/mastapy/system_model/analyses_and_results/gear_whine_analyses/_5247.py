'''_5247.py

BoltedJointGearWhineAnalysis
'''


from mastapy.system_model.part_model import _1965
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6042
from mastapy.system_model.analyses_and_results.system_deflections import _2201
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5342
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'BoltedJointGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointGearWhineAnalysis',)


class BoltedJointGearWhineAnalysis(_5342.SpecialisedAssemblyGearWhineAnalysis):
    '''BoltedJointGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1965.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6042.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6042.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2201.BoltedJointSystemDeflection':
        '''BoltedJointSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2201.BoltedJointSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
