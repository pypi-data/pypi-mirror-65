'''_3642.py

CylindricalGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2064
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3640, _3641, _3652
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3505
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CylindricalGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundParametricStudyTool',)


class CylindricalGearSetCompoundParametricStudyTool(_3652.GearSetCompoundParametricStudyTool):
    '''CylindricalGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2064.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2064.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_parametric_study_tool(self) -> 'List[_3640.CylindricalGearCompoundParametricStudyTool]':
        '''List[CylindricalGearCompoundParametricStudyTool]: 'CylindricalGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundParametricStudyTool, constructor.new(_3640.CylindricalGearCompoundParametricStudyTool))
        return value

    @property
    def cylindrical_meshes_compound_parametric_study_tool(self) -> 'List[_3641.CylindricalGearMeshCompoundParametricStudyTool]':
        '''List[CylindricalGearMeshCompoundParametricStudyTool]: 'CylindricalMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundParametricStudyTool, constructor.new(_3641.CylindricalGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3505.CylindricalGearSetParametricStudyTool]':
        '''List[CylindricalGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3505.CylindricalGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3505.CylindricalGearSetParametricStudyTool]':
        '''List[CylindricalGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3505.CylindricalGearSetParametricStudyTool))
        return value
