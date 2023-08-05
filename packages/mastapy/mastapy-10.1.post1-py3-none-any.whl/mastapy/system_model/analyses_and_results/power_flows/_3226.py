'''_3226.py

BevelDifferentialGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2054
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6058
from mastapy.gears.rating.bevel import _342
from mastapy.gears.rating.zerol_bevel import _174
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.straight_bevel import _204
from mastapy.gears.rating.spiral_bevel import _207
from mastapy.system_model.analyses_and_results.power_flows import _3225, _3224, _3231
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BevelDifferentialGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetPowerFlow',)


class BevelDifferentialGearSetPowerFlow(_3231.BevelGearSetPowerFlow):
    '''BevelDifferentialGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2054.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2054.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6058.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6058.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_342.BevelGearSetRating':
        '''BevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_342.BevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_set_rating(self) -> '_174.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _174.ZerolBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_174.ZerolBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_set_rating(self) -> '_204.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _204.StraightBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_204.StraightBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_set_rating(self) -> '_207.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _207.SpiralBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_207.SpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_342.BevelGearSetRating':
        '''BevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_342.BevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_zerol_bevel_gear_set_rating(self) -> '_174.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _174.ZerolBevelGearSetRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_174.ZerolBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_straight_bevel_gear_set_rating(self) -> '_204.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _204.StraightBevelGearSetRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_204.StraightBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spiral_bevel_gear_set_rating(self) -> '_207.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _207.SpiralBevelGearSetRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_207.SpiralBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3225.BevelDifferentialGearPowerFlow]':
        '''List[BevelDifferentialGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3225.BevelDifferentialGearPowerFlow))
        return value

    @property
    def bevel_differential_gears_power_flow(self) -> 'List[_3225.BevelDifferentialGearPowerFlow]':
        '''List[BevelDifferentialGearPowerFlow]: 'BevelDifferentialGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsPowerFlow, constructor.new(_3225.BevelDifferentialGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3224.BevelDifferentialGearMeshPowerFlow]':
        '''List[BevelDifferentialGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3224.BevelDifferentialGearMeshPowerFlow))
        return value

    @property
    def bevel_differential_meshes_power_flow(self) -> 'List[_3224.BevelDifferentialGearMeshPowerFlow]':
        '''List[BevelDifferentialGearMeshPowerFlow]: 'BevelDifferentialMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesPowerFlow, constructor.new(_3224.BevelDifferentialGearMeshPowerFlow))
        return value
