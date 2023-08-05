'''_5774.py

TorqueConverterConnectionCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1903
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5384
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5700
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'TorqueConverterConnectionCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundGearWhineAnalysis',)


class TorqueConverterConnectionCompoundGearWhineAnalysis(_5700.CouplingConnectionCompoundGearWhineAnalysis):
    '''TorqueConverterConnectionCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1903.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1903.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1903.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1903.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5384.TorqueConverterConnectionGearWhineAnalysis]':
        '''List[TorqueConverterConnectionGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5384.TorqueConverterConnectionGearWhineAnalysis))
        return value

    @property
    def connection_gear_whine_analysis_load_cases(self) -> 'List[_5384.TorqueConverterConnectionGearWhineAnalysis]':
        '''List[TorqueConverterConnectionGearWhineAnalysis]: 'ConnectionGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionGearWhineAnalysisLoadCases, constructor.new(_5384.TorqueConverterConnectionGearWhineAnalysis))
        return value
