'''_3671.py

OilSealCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3541
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3633
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'OilSealCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundParametricStudyTool',)


class OilSealCompoundParametricStudyTool(_3633.ConnectorCompoundParametricStudyTool):
    '''OilSealCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3541.OilSealParametricStudyTool]':
        '''List[OilSealParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3541.OilSealParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3541.OilSealParametricStudyTool]':
        '''List[OilSealParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3541.OilSealParametricStudyTool))
        return value
