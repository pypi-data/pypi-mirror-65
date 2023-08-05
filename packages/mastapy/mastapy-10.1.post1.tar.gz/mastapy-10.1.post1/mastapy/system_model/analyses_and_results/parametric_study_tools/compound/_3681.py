'''_3681.py

PulleyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2123
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3560
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3636
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PulleyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundParametricStudyTool',)


class PulleyCompoundParametricStudyTool(_3636.CouplingHalfCompoundParametricStudyTool):
    '''PulleyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2123.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2123.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3560.PulleyParametricStudyTool]':
        '''List[PulleyParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3560.PulleyParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3560.PulleyParametricStudyTool]':
        '''List[PulleyParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3560.PulleyParametricStudyTool))
        return value
