'''_3450.py

TorqueConverterCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2139
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3329
from mastapy.system_model.analyses_and_results.power_flows.compound import _3376
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundPowerFlow',)


class TorqueConverterCompoundPowerFlow(_3376.CouplingCompoundPowerFlow):
    '''TorqueConverterCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2139.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2139.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3329.TorqueConverterPowerFlow]':
        '''List[TorqueConverterPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3329.TorqueConverterPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3329.TorqueConverterPowerFlow]':
        '''List[TorqueConverterPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3329.TorqueConverterPowerFlow))
        return value
