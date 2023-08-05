'''_3951.py

BeltDriveModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2088
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6033
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4036
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'BeltDriveModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveModalAnalysesAtSpeeds',)


class BeltDriveModalAnalysesAtSpeeds(_4036.SpecialisedAssemblyModalAnalysesAtSpeeds):
    '''BeltDriveModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveModalAnalysesAtSpeeds.TYPE'):
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
