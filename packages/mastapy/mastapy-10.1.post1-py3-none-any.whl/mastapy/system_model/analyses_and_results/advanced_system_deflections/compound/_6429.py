'''_6429.py

MeasurementComponentCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2004
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6306
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6473
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'MeasurementComponentCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundAdvancedSystemDeflection',)


class MeasurementComponentCompoundAdvancedSystemDeflection(_6473.VirtualComponentCompoundAdvancedSystemDeflection):
    '''MeasurementComponentCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2004.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6306.MeasurementComponentAdvancedSystemDeflection]':
        '''List[MeasurementComponentAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6306.MeasurementComponentAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6306.MeasurementComponentAdvancedSystemDeflection]':
        '''List[MeasurementComponentAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6306.MeasurementComponentAdvancedSystemDeflection))
        return value
