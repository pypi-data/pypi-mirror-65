'''_3541.py

OilSealParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6152
from mastapy.system_model.analyses_and_results.system_deflections import _2290
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3496
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'OilSealParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealParametricStudyTool',)


class OilSealParametricStudyTool(_3496.ConnectorParametricStudyTool):
    '''OilSealParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6152.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6152.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2290.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2290.OilSealSystemDeflection))
        return value
