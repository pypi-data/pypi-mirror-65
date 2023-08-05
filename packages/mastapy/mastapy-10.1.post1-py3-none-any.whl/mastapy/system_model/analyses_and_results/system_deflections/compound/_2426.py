'''_2426.py

OilSealCompoundSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2007
from mastapy.system_model.analyses_and_results.system_deflections import _2290
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2388
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'OilSealCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundSystemDeflection',)


class OilSealCompoundSystemDeflection(_2388.ConnectorCompoundSystemDeflection):
    '''OilSealCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def reliability_for_oil_seal(self) -> 'float':
        '''float: 'ReliabilityForOilSeal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReliabilityForOilSeal

    @property
    def component_design(self) -> '_2007.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2290.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2290.OilSealSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2290.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2290.OilSealSystemDeflection))
        return value
