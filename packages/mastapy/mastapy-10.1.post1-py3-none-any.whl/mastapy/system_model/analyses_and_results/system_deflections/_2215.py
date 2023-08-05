'''_2215.py

BevelDifferentialGearMeshSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.gears import _1861
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6057
from mastapy.system_model.analyses_and_results.power_flows import _3224
from mastapy.gears.rating.bevel import _340
from mastapy.gears.rating.zerol_bevel import _172
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.straight_bevel import _202
from mastapy.gears.rating.spiral_bevel import _205
from mastapy.system_model.analyses_and_results.system_deflections import _2220
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BevelDifferentialGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshSystemDeflection',)


class BevelDifferentialGearMeshSystemDeflection(_2220.BevelGearMeshSystemDeflection):
    '''BevelDifferentialGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1861.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1861.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6057.BevelDifferentialGearMeshLoadCase':
        '''BevelDifferentialGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6057.BevelDifferentialGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3224.BevelDifferentialGearMeshPowerFlow':
        '''BevelDifferentialGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3224.BevelDifferentialGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_340.BevelGearMeshRating':
        '''BevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_340.BevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_mesh_rating(self) -> '_172.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _172.ZerolBevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ZerolBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_172.ZerolBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_mesh_rating(self) -> '_202.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _202.StraightBevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_202.StraightBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_mesh_rating(self) -> '_205.SpiralBevelGearMeshRating':
        '''SpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _205.SpiralBevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to SpiralBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_205.SpiralBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_340.BevelGearMeshRating':
        '''BevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_340.BevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_zerol_bevel_gear_mesh_rating(self) -> '_172.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _172.ZerolBevelGearMeshRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to ZerolBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_172.ZerolBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_straight_bevel_gear_mesh_rating(self) -> '_202.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _202.StraightBevelGearMeshRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to StraightBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_202.StraightBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spiral_bevel_gear_mesh_rating(self) -> '_205.SpiralBevelGearMeshRating':
        '''SpiralBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _205.SpiralBevelGearMeshRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SpiralBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_205.SpiralBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
