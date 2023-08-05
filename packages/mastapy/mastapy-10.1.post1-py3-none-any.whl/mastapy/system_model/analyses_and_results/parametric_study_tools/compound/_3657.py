'''_3657.py

ImportedFEComponentCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2000
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3526
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3600
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ImportedFEComponentCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentCompoundParametricStudyTool',)


class ImportedFEComponentCompoundParametricStudyTool(_3600.AbstractShaftOrHousingCompoundParametricStudyTool):
    '''ImportedFEComponentCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2000.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2000.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3526.ImportedFEComponentParametricStudyTool]':
        '''List[ImportedFEComponentParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3526.ImportedFEComponentParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3526.ImportedFEComponentParametricStudyTool]':
        '''List[ImportedFEComponentParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3526.ImportedFEComponentParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[ImportedFEComponentCompoundParametricStudyTool]':
        '''List[ImportedFEComponentCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentCompoundParametricStudyTool))
        return value
