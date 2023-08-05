'''_2299.py

PulleySystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2123
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6166
from mastapy.system_model.analyses_and_results.power_flows import _3300
from mastapy.system_model.analyses_and_results.system_deflections import _2244
from mastapy._internal.python_net import python_net_import

_PULLEY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PulleySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleySystemDeflection',)


class PulleySystemDeflection(_2244.CouplingHalfSystemDeflection):
    '''PulleySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PULLEY_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2123.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2123.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6166.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6166.PulleyLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3300.PulleyPowerFlow':
        '''PulleyPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3300.PulleyPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
