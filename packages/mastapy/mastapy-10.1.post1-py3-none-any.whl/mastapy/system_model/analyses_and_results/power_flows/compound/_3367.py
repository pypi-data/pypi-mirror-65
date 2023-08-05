'''_3367.py

ConceptCouplingHalfCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3240
from mastapy.system_model.analyses_and_results.power_flows.compound import _3378
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConceptCouplingHalfCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundPowerFlow',)


class ConceptCouplingHalfCompoundPowerFlow(_3378.CouplingHalfCompoundPowerFlow):
    '''ConceptCouplingHalfCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2116.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3240.ConceptCouplingHalfPowerFlow]':
        '''List[ConceptCouplingHalfPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3240.ConceptCouplingHalfPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3240.ConceptCouplingHalfPowerFlow]':
        '''List[ConceptCouplingHalfPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3240.ConceptCouplingHalfPowerFlow))
        return value
