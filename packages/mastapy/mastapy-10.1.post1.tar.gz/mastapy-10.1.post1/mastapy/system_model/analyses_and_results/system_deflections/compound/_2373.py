'''_2373.py

ClutchCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2112
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2227
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2389
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ClutchCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundSystemDeflection',)


class ClutchCompoundSystemDeflection(_2389.CouplingCompoundSystemDeflection):
    '''ClutchCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2112.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2112.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2112.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2112.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2227.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2227.ClutchSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2227.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2227.ClutchSystemDeflection))
        return value
