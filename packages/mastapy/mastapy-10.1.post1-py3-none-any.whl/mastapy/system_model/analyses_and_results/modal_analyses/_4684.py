'''_4684.py

BeltDriveModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2088
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6033
from mastapy.system_model.analyses_and_results.system_deflections import _2192
from mastapy.system_model.analyses_and_results.modal_analyses import _4774
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BeltDriveModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveModalAnalysis',)


class BeltDriveModalAnalysis(_4774.SpecialisedAssemblyModalAnalysis):
    '''BeltDriveModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2088.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6033.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6033.BeltDriveLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2192.BeltDriveSystemDeflection':
        '''BeltDriveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.BeltDriveSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
