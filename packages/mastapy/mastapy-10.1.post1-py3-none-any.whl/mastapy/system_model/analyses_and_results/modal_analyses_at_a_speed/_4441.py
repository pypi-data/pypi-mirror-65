'''_4441.py

BeltDriveModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2088
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6033
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4524
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'BeltDriveModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveModalAnalysisAtASpeed',)


class BeltDriveModalAnalysisAtASpeed(_4524.SpecialisedAssemblyModalAnalysisAtASpeed):
    '''BeltDriveModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveModalAnalysisAtASpeed.TYPE'):
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
