'''_6353.py

WormGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2089
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6208
from mastapy.gears.rating.worm import _177
from mastapy.system_model.analyses_and_results.system_deflections import _2341
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6286
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'WormGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearAdvancedSystemDeflection',)


class WormGearAdvancedSystemDeflection(_6286.GearAdvancedSystemDeflection):
    '''WormGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2089.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6208.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6208.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_177.WormGearRating':
        '''WormGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_177.WormGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_system_deflection_results(self) -> 'List[_2341.WormGearSystemDeflection]':
        '''List[WormGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2341.WormGearSystemDeflection))
        return value
