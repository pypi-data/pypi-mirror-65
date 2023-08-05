'''_3266.py

FlexiblePinAssemblyPowerFlow
'''


from mastapy.system_model.part_model import _1996
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6115
from mastapy.system_model.analyses_and_results.power_flows import _3308
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FlexiblePinAssemblyPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyPowerFlow',)


class FlexiblePinAssemblyPowerFlow(_3308.SpecialisedAssemblyPowerFlow):
    '''FlexiblePinAssemblyPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1996.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6115.FlexiblePinAssemblyLoadCase':
        '''FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6115.FlexiblePinAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
