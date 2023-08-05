'''_6324.py

ShaftHubConnectionAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2131
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6172
from mastapy.system_model.analyses_and_results.system_deflections import _2304
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6268
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ShaftHubConnectionAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionAdvancedSystemDeflection',)


class ShaftHubConnectionAdvancedSystemDeflection(_6268.ConnectorAdvancedSystemDeflection):
    '''ShaftHubConnectionAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2131.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2131.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6172.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6172.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionAdvancedSystemDeflection]':
        '''List[ShaftHubConnectionAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionAdvancedSystemDeflection))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2304.ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2304.ShaftHubConnectionSystemDeflection))
        return value
