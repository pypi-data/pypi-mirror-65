'''_2282.py

KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2079
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6146
from mastapy.system_model.analyses_and_results.power_flows import _3284
from mastapy.gears.rating.klingelnberg_spiral_bevel import _210
from mastapy.system_model.analyses_and_results.system_deflections import _2283, _2281, _2276
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection',)


class KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection(_2276.KlingelnbergCycloPalloidConicalGearSetSystemDeflection):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2079.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2079.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6146.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6146.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3284.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3284.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_210.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_210.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_210.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_210.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_system_deflection(self) -> 'List[_2283.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsSystemDeflection, constructor.new(_2283.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_system_deflection(self) -> 'List[_2281.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesSystemDeflection, constructor.new(_2281.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection))
        return value
