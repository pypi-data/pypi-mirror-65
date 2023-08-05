'''_3559.py

PowerLoadParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2012
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6165
from mastapy.system_model.analyses_and_results.system_deflections import _2298
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3592
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'PowerLoadParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadParametricStudyTool',)


class PowerLoadParametricStudyTool(_3592.VirtualComponentParametricStudyTool):
    '''PowerLoadParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2012.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6165.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6165.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2298.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2298.PowerLoadSystemDeflection))
        return value
