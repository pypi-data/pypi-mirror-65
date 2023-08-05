'''_5861.py

KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2077
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6143
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5859, _5860, _5858
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis(_5858.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis.TYPE'):
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
    def klingelnberg_cyclo_palloid_hypoid_gears_dynamic_analysis(self) -> 'List[_5859.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsDynamicAnalysis, constructor.new(_5859.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_dynamic_analysis(self) -> 'List[_5860.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesDynamicAnalysis, constructor.new(_5860.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis))
        return value
