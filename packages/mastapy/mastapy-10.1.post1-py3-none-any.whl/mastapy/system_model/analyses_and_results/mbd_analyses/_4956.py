'''_4956.py

BevelDifferentialGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2032
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6036
from mastapy.system_model.analyses_and_results.mbd_analyses import _4955, _4954, _4961
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BevelDifferentialGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetMultiBodyDynamicsAnalysis',)


class BevelDifferentialGearSetMultiBodyDynamicsAnalysis(_4961.BevelGearSetMultiBodyDynamicsAnalysis):
    '''BevelDifferentialGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2032.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6036.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6036.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_4955.BevelDifferentialGearMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_4955.BevelDifferentialGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gears_multi_body_dynamics_analysis(self) -> 'List[_4955.BevelDifferentialGearMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMultiBodyDynamicsAnalysis]: 'BevelDifferentialGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsMultiBodyDynamicsAnalysis, constructor.new(_4955.BevelDifferentialGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_meshes_multi_body_dynamics_analysis(self) -> 'List[_4954.BevelDifferentialGearMeshMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMeshMultiBodyDynamicsAnalysis]: 'BevelDifferentialMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesMultiBodyDynamicsAnalysis, constructor.new(_4954.BevelDifferentialGearMeshMultiBodyDynamicsAnalysis))
        return value
