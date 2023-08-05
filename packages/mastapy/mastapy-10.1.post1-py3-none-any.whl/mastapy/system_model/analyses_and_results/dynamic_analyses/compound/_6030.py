'''_6030.py

UnbalancedMassCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2017
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5909
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6031
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'UnbalancedMassCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundDynamicAnalysis',)


class UnbalancedMassCompoundDynamicAnalysis(_6031.VirtualComponentCompoundDynamicAnalysis):
    '''UnbalancedMassCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2017.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5909.UnbalancedMassDynamicAnalysis]':
        '''List[UnbalancedMassDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5909.UnbalancedMassDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5909.UnbalancedMassDynamicAnalysis]':
        '''List[UnbalancedMassDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5909.UnbalancedMassDynamicAnalysis))
        return value
