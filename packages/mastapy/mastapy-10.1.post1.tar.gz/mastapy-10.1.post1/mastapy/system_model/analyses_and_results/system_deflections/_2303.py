'''_2303.py

RootAssemblySystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2014
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2328, _2230, _2211
from mastapy.system_model.analyses_and_results.power_flows import _3304
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'RootAssemblySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblySystemDeflection',)


class RootAssemblySystemDeflection(_2211.AssemblySystemDeflection):
    '''RootAssemblySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2014.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def system_deflection_inputs(self) -> '_2328.SystemDeflection':
        '''SystemDeflection: 'SystemDeflectionInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2328.SystemDeflection)(self.wrapped.SystemDeflectionInputs) if self.wrapped.SystemDeflectionInputs else None

    @property
    def power_flow_results(self) -> '_3304.RootAssemblyPowerFlow':
        '''RootAssemblyPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3304.RootAssemblyPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def shaft_deflection_results(self) -> 'List[_2230.ConcentricPartGroupCombinationSystemDeflectionResults]':
        '''List[ConcentricPartGroupCombinationSystemDeflectionResults]: 'ShaftDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftDeflectionResults, constructor.new(_2230.ConcentricPartGroupCombinationSystemDeflectionResults))
        return value
