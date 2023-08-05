'''_2431.py

PlanetaryConnectionCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1847
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2444
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PlanetaryConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundSystemDeflection',)


class PlanetaryConnectionCompoundSystemDeflection(_2444.ShaftToMountableComponentConnectionCompoundSystemDeflection):
    '''PlanetaryConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1847.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1847.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1847.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1847.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2295.PlanetaryConnectionSystemDeflection]':
        '''List[PlanetaryConnectionSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2295.PlanetaryConnectionSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2295.PlanetaryConnectionSystemDeflection]':
        '''List[PlanetaryConnectionSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2295.PlanetaryConnectionSystemDeflection))
        return value
