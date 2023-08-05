'''_2430.py

PartToPartShearCouplingHalfCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2122
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2293
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2391
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PartToPartShearCouplingHalfCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfCompoundSystemDeflection',)


class PartToPartShearCouplingHalfCompoundSystemDeflection(_2391.CouplingHalfCompoundSystemDeflection):
    '''PartToPartShearCouplingHalfCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2122.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2293.PartToPartShearCouplingHalfSystemDeflection]':
        '''List[PartToPartShearCouplingHalfSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2293.PartToPartShearCouplingHalfSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2293.PartToPartShearCouplingHalfSystemDeflection]':
        '''List[PartToPartShearCouplingHalfSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2293.PartToPartShearCouplingHalfSystemDeflection))
        return value
