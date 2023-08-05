'''_5989.py

OilSealCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5868
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5951
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'OilSealCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundDynamicAnalysis',)


class OilSealCompoundDynamicAnalysis(_5951.ConnectorCompoundDynamicAnalysis):
    '''OilSealCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5868.OilSealDynamicAnalysis]':
        '''List[OilSealDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5868.OilSealDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5868.OilSealDynamicAnalysis]':
        '''List[OilSealDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5868.OilSealDynamicAnalysis))
        return value
