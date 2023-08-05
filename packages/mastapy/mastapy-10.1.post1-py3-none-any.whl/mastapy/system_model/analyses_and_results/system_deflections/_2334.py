'''_2334.py

TorqueConverterTurbineSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2142
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6201
from mastapy.system_model.analyses_and_results.power_flows import _3331
from mastapy.system_model.analyses_and_results.system_deflections import _2244
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'TorqueConverterTurbineSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineSystemDeflection',)


class TorqueConverterTurbineSystemDeflection(_2244.CouplingHalfSystemDeflection):
    '''TorqueConverterTurbineSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2142.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6201.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6201.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3331.TorqueConverterTurbinePowerFlow':
        '''TorqueConverterTurbinePowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3331.TorqueConverterTurbinePowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
