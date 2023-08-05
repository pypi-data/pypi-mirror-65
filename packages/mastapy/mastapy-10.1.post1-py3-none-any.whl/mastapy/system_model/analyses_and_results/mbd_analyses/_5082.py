'''_5082.py

StraightBevelGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6189
from mastapy.system_model.analyses_and_results.mbd_analyses import _5081, _5080, _4983
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetMultiBodyDynamicsAnalysis',)


class StraightBevelGearSetMultiBodyDynamicsAnalysis(_4983.BevelGearSetMultiBodyDynamicsAnalysis):
    '''StraightBevelGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetMultiBodyDynamicsAnalysis.TYPE'):
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
    def gears(self) -> 'List[_5081.StraightBevelGearMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5081.StraightBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gears_multi_body_dynamics_analysis(self) -> 'List[_5081.StraightBevelGearMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearMultiBodyDynamicsAnalysis]: 'StraightBevelGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsMultiBodyDynamicsAnalysis, constructor.new(_5081.StraightBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_meshes_multi_body_dynamics_analysis(self) -> 'List[_5080.StraightBevelGearMeshMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearMeshMultiBodyDynamicsAnalysis]: 'StraightBevelMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesMultiBodyDynamicsAnalysis, constructor.new(_5080.StraightBevelGearMeshMultiBodyDynamicsAnalysis))
        return value
