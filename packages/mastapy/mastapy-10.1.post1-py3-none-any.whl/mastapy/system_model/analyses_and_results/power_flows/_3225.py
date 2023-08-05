'''_3225.py

BevelDifferentialGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2053
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6056
from mastapy.gears.rating.bevel import _341
from mastapy.gears.rating.zerol_bevel import _173
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.straight_bevel import _203
from mastapy.gears.rating.spiral_bevel import _206
from mastapy.system_model.analyses_and_results.power_flows import _3230
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BevelDifferentialGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearPowerFlow',)


class BevelDifferentialGearPowerFlow(_3230.BevelGearPowerFlow):
    '''BevelDifferentialGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2053.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2053.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6056.BevelDifferentialGearLoadCase':
        '''BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6056.BevelDifferentialGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_341.BevelGearRating':
        '''BevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_341.BevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_zerol_bevel_gear_rating(self) -> '_173.ZerolBevelGearRating':
        '''ZerolBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _173.ZerolBevelGearRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to ZerolBevelGearRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_173.ZerolBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_straight_bevel_gear_rating(self) -> '_203.StraightBevelGearRating':
        '''StraightBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _203.StraightBevelGearRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to StraightBevelGearRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_203.StraightBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spiral_bevel_gear_rating(self) -> '_206.SpiralBevelGearRating':
        '''SpiralBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _206.SpiralBevelGearRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SpiralBevelGearRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_206.SpiralBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
