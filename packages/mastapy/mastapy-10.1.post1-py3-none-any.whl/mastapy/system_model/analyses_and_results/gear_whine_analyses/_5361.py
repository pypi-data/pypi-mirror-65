'''_5361.py

ShaftHubConnectionGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2131
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6172
from mastapy.system_model.analyses_and_results.system_deflections import _2304
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5287
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ShaftHubConnectionGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionGearWhineAnalysis',)


class ShaftHubConnectionGearWhineAnalysis(_5287.ConnectorGearWhineAnalysis):
    '''ShaftHubConnectionGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionGearWhineAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2304.ShaftHubConnectionSystemDeflection':
        '''ShaftHubConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2304.ShaftHubConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionGearWhineAnalysis]':
        '''List[ShaftHubConnectionGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionGearWhineAnalysis))
        return value
