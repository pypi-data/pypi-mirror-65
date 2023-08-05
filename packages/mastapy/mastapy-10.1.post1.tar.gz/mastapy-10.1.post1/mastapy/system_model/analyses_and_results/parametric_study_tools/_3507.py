'''_3507.py

DatumParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1992
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6098
from mastapy.system_model.analyses_and_results.system_deflections import _2259
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3485
from mastapy._internal.python_net import python_net_import

_DATUM_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DatumParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumParametricStudyTool',)


class DatumParametricStudyTool(_3485.ComponentParametricStudyTool):
    '''DatumParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _DATUM_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1992.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1992.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6098.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6098.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2259.DatumSystemDeflection]':
        '''List[DatumSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2259.DatumSystemDeflection))
        return value
