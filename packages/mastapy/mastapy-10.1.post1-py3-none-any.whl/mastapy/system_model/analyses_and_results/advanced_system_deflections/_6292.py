'''_6292.py

HypoidGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2073
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6134
from mastapy.gears.rating.hypoid import _243
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6290, _6291, _6238
from mastapy.system_model.analyses_and_results.system_deflections import _2271
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'HypoidGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetAdvancedSystemDeflection',)


class HypoidGearSetAdvancedSystemDeflection(_6238.AGMAGleasonConicalGearSetAdvancedSystemDeflection):
    '''HypoidGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2073.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2073.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6134.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6134.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_243.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_243.HypoidGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_243.HypoidGearSetRating':
        '''HypoidGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_243.HypoidGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def hypoid_gears_advanced_system_deflection(self) -> 'List[_6290.HypoidGearAdvancedSystemDeflection]':
        '''List[HypoidGearAdvancedSystemDeflection]: 'HypoidGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsAdvancedSystemDeflection, constructor.new(_6290.HypoidGearAdvancedSystemDeflection))
        return value

    @property
    def hypoid_meshes_advanced_system_deflection(self) -> 'List[_6291.HypoidGearMeshAdvancedSystemDeflection]':
        '''List[HypoidGearMeshAdvancedSystemDeflection]: 'HypoidMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesAdvancedSystemDeflection, constructor.new(_6291.HypoidGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2271.HypoidGearSetSystemDeflection]':
        '''List[HypoidGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2271.HypoidGearSetSystemDeflection))
        return value
