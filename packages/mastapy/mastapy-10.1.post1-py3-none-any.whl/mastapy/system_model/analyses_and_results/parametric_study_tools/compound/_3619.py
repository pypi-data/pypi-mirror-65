'''_3619.py

ClutchConnectionCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1893
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3481
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3635
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ClutchConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundParametricStudyTool',)


class ClutchConnectionCompoundParametricStudyTool(_3635.CouplingConnectionCompoundParametricStudyTool):
    '''ClutchConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1893.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1893.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1893.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1893.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3481.ClutchConnectionParametricStudyTool]':
        '''List[ClutchConnectionParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3481.ClutchConnectionParametricStudyTool))
        return value

    @property
    def connection_parametric_study_tool_load_cases(self) -> 'List[_3481.ClutchConnectionParametricStudyTool]':
        '''List[ClutchConnectionParametricStudyTool]: 'ConnectionParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionParametricStudyToolLoadCases, constructor.new(_3481.ClutchConnectionParametricStudyTool))
        return value
