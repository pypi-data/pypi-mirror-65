'''_5099.py

BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2032
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5097, _5098, _5104
from mastapy.system_model.analyses_and_results.mbd_analyses import _4956
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis',)


class BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis(_5104.BevelGearSetCompoundMultiBodyDynamicsAnalysis):
    '''BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
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
    def bevel_differential_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_5097.BevelDifferentialGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearCompoundMultiBodyDynamicsAnalysis]: 'BevelDifferentialGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_5097.BevelDifferentialGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_5098.BevelDifferentialGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundMultiBodyDynamicsAnalysis]: 'BevelDifferentialMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_5098.BevelDifferentialGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4956.BevelDifferentialGearSetMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4956.BevelDifferentialGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_4956.BevelDifferentialGearSetMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_4956.BevelDifferentialGearSetMultiBodyDynamicsAnalysis))
        return value
