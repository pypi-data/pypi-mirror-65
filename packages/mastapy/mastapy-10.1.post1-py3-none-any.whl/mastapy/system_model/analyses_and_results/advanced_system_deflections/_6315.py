'''_6315.py

PlanetCarrierAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2009
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6161
from mastapy.system_model.analyses_and_results.system_deflections import _2296
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6307
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'PlanetCarrierAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierAdvancedSystemDeflection',)


class PlanetCarrierAdvancedSystemDeflection(_6307.MountableComponentAdvancedSystemDeflection):
    '''PlanetCarrierAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2009.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6161.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6161.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2296.PlanetCarrierSystemDeflection]':
        '''List[PlanetCarrierSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2296.PlanetCarrierSystemDeflection))
        return value
