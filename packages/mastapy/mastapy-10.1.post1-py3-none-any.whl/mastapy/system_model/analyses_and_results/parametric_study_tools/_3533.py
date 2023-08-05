'''_3533.py

KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2077
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6143
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3532, _3531, _3530
from mastapy.system_model.analyses_and_results.system_deflections import _2279
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool',)


class KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool(_3530.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool):
    '''KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2077.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2077.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6143.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6143.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_parametric_study_tool(self) -> 'List[_3532.KlingelnbergCycloPalloidHypoidGearParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsParametricStudyTool, constructor.new(_3532.KlingelnbergCycloPalloidHypoidGearParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_parametric_study_tool(self) -> 'List[_3531.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesParametricStudyTool, constructor.new(_3531.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2279.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2279.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection))
        return value
