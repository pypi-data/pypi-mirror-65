'''_6384.py

ConceptCouplingConnectionCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1895
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6259
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6395
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ConceptCouplingConnectionCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionCompoundAdvancedSystemDeflection',)


class ConceptCouplingConnectionCompoundAdvancedSystemDeflection(_6395.CouplingConnectionCompoundAdvancedSystemDeflection):
    '''ConceptCouplingConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1895.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1895.ConceptCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1895.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1895.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6259.ConceptCouplingConnectionAdvancedSystemDeflection]':
        '''List[ConceptCouplingConnectionAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6259.ConceptCouplingConnectionAdvancedSystemDeflection))
        return value

    @property
    def connection_advanced_system_deflection_load_cases(self) -> 'List[_6259.ConceptCouplingConnectionAdvancedSystemDeflection]':
        '''List[ConceptCouplingConnectionAdvancedSystemDeflection]: 'ConnectionAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedSystemDeflectionLoadCases, constructor.new(_6259.ConceptCouplingConnectionAdvancedSystemDeflection))
        return value
