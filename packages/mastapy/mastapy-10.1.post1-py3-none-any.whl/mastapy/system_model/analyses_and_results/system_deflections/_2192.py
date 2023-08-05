'''_2192.py

BeltDriveSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2088
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6033
from mastapy.system_model.analyses_and_results.power_flows import _3201
from mastapy.system_model.analyses_and_results.system_deflections import _2191, _2287
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BeltDriveSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveSystemDeflection',)


class BeltDriveSystemDeflection(_2287.SpecialisedAssemblySystemDeflection):
    '''BeltDriveSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveSystemDeflection.TYPE'):
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
    def power_flow_results(self) -> '_3201.BeltDrivePowerFlow':
        '''BeltDrivePowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3201.BeltDrivePowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def belts(self) -> 'List[_2191.BeltConnectionSystemDeflection]':
        '''List[BeltConnectionSystemDeflection]: 'Belts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Belts, constructor.new(_2191.BeltConnectionSystemDeflection))
        return value
