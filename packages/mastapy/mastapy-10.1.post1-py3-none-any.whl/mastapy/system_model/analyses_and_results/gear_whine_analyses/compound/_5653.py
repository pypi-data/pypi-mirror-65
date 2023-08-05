'''_5653.py

BevelDifferentialGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2032
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5651, _5652, _5658
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5241
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'BevelDifferentialGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundGearWhineAnalysis',)


class BevelDifferentialGearSetCompoundGearWhineAnalysis(_5658.BevelGearSetCompoundGearWhineAnalysis):
    '''BevelDifferentialGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2032.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2032.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_gear_whine_analysis(self) -> 'List[_5651.BevelDifferentialGearCompoundGearWhineAnalysis]':
        '''List[BevelDifferentialGearCompoundGearWhineAnalysis]: 'BevelDifferentialGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundGearWhineAnalysis, constructor.new(_5651.BevelDifferentialGearCompoundGearWhineAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_gear_whine_analysis(self) -> 'List[_5652.BevelDifferentialGearMeshCompoundGearWhineAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundGearWhineAnalysis]: 'BevelDifferentialMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundGearWhineAnalysis, constructor.new(_5652.BevelDifferentialGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5241.BevelDifferentialGearSetGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5241.BevelDifferentialGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5241.BevelDifferentialGearSetGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5241.BevelDifferentialGearSetGearWhineAnalysis))
        return value
