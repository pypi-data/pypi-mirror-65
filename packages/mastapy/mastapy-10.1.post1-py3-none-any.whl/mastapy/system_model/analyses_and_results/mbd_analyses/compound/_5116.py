'''_5116.py

BearingCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _4972
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5144
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'BearingCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundMultiBodyDynamicsAnalysis',)


class BearingCompoundMultiBodyDynamicsAnalysis(_5144.ConnectorCompoundMultiBodyDynamicsAnalysis):
    '''BearingCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1984.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4972.BearingMultiBodyDynamicsAnalysis]':
        '''List[BearingMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4972.BearingMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_4972.BearingMultiBodyDynamicsAnalysis]':
        '''List[BearingMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_4972.BearingMultiBodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundMultiBodyDynamicsAnalysis]':
        '''List[BearingCompoundMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundMultiBodyDynamicsAnalysis))
        return value
