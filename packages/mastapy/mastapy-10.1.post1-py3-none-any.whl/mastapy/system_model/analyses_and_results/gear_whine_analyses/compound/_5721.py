'''_5721.py

HypoidGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2073
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5719, _5720, _5668
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5329
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'HypoidGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundGearWhineAnalysis',)


class HypoidGearSetCompoundGearWhineAnalysis(_5668.AGMAGleasonConicalGearSetCompoundGearWhineAnalysis):
    '''HypoidGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2073.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2073.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2073.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2073.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_gear_whine_analysis(self) -> 'List[_5719.HypoidGearCompoundGearWhineAnalysis]':
        '''List[HypoidGearCompoundGearWhineAnalysis]: 'HypoidGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundGearWhineAnalysis, constructor.new(_5719.HypoidGearCompoundGearWhineAnalysis))
        return value

    @property
    def hypoid_meshes_compound_gear_whine_analysis(self) -> 'List[_5720.HypoidGearMeshCompoundGearWhineAnalysis]':
        '''List[HypoidGearMeshCompoundGearWhineAnalysis]: 'HypoidMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundGearWhineAnalysis, constructor.new(_5720.HypoidGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5329.HypoidGearSetGearWhineAnalysis]':
        '''List[HypoidGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5329.HypoidGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5329.HypoidGearSetGearWhineAnalysis]':
        '''List[HypoidGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5329.HypoidGearSetGearWhineAnalysis))
        return value
