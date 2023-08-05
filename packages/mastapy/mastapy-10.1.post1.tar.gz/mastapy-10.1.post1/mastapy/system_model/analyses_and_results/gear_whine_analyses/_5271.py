'''_5271.py

ClutchConnectionGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _1893
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6066
from mastapy.system_model.analyses_and_results.system_deflections import _2225
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5288
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ClutchConnectionGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionGearWhineAnalysis',)


class ClutchConnectionGearWhineAnalysis(_5288.CouplingConnectionGearWhineAnalysis):
    '''ClutchConnectionGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1893.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1893.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6066.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6066.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2225.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ClutchConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
