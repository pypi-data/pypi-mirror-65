'''_5898.py

StraightBevelGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6189
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5896, _5897, _5810
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'StraightBevelGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetDynamicAnalysis',)


class StraightBevelGearSetDynamicAnalysis(_5810.BevelGearSetDynamicAnalysis):
    '''StraightBevelGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2086.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6189.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6189.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_dynamic_analysis(self) -> 'List[_5896.StraightBevelGearDynamicAnalysis]':
        '''List[StraightBevelGearDynamicAnalysis]: 'StraightBevelGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsDynamicAnalysis, constructor.new(_5896.StraightBevelGearDynamicAnalysis))
        return value

    @property
    def straight_bevel_meshes_dynamic_analysis(self) -> 'List[_5897.StraightBevelGearMeshDynamicAnalysis]':
        '''List[StraightBevelGearMeshDynamicAnalysis]: 'StraightBevelMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesDynamicAnalysis, constructor.new(_5897.StraightBevelGearMeshDynamicAnalysis))
        return value
