'''_2203.py

ClutchConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.couplings import _1872
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6044
from mastapy.system_model.analyses_and_results.power_flows import _3212
from mastapy.system_model.analyses_and_results.system_deflections import _2221
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ClutchConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionSystemDeflection',)


class ClutchConnectionSystemDeflection(_2221.CouplingConnectionSystemDeflection):
    '''ClutchConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1872.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1872.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6044.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6044.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3212.ClutchConnectionPowerFlow':
        '''ClutchConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3212.ClutchConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
