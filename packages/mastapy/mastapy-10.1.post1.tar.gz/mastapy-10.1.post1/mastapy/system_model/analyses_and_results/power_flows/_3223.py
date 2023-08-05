'''_3223.py

BeltDrivePowerFlow
'''


from mastapy.system_model.part_model.couplings import _2110
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6055
from mastapy.system_model.analyses_and_results.power_flows import _3308
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BeltDrivePowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDrivePowerFlow',)


class BeltDrivePowerFlow(_3308.SpecialisedAssemblyPowerFlow):
    '''BeltDrivePowerFlow

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDrivePowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2110.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6055.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6055.BeltDriveLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
