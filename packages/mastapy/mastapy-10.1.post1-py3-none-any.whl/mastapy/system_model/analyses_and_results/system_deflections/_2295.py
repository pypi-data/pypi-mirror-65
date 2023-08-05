'''_2295.py

PlanetaryConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets import _1847
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6158
from mastapy.system_model.analyses_and_results.power_flows import _3293
from mastapy.system_model.analyses_and_results.system_deflections import _2308
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PlanetaryConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionSystemDeflection',)


class PlanetaryConnectionSystemDeflection(_2308.ShaftToMountableComponentConnectionSystemDeflection):
    '''PlanetaryConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1847.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1847.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6158.PlanetaryConnectionLoadCase':
        '''PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6158.PlanetaryConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3293.PlanetaryConnectionPowerFlow':
        '''PlanetaryConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3293.PlanetaryConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
