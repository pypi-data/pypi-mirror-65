'''_2296.py

PlanetCarrierSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2009
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6161
from mastapy.system_model.analyses_and_results.power_flows import _3295
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2349
from mastapy.system_model.analyses_and_results.system_deflections import _2288
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PlanetCarrierSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierSystemDeflection',)


class PlanetCarrierSystemDeflection(_2288.MountableComponentSystemDeflection):
    '''PlanetCarrierSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierSystemDeflection.TYPE'):
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
    def power_flow_results(self) -> '_3295.PlanetCarrierPowerFlow':
        '''PlanetCarrierPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3295.PlanetCarrierPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def windup(self) -> 'List[_2349.PlanetCarrierWindup]':
        '''List[PlanetCarrierWindup]: 'Windup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Windup, constructor.new(_2349.PlanetCarrierWindup))
        return value
