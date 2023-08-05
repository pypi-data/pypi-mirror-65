'''_5059.py

PulleyMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2123
from mastapy.system_model.analyses_and_results.static_loads import _6166
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5107
from mastapy.system_model.analyses_and_results.mbd_analyses import _5004
from mastapy._internal.python_net import python_net_import

_PULLEY_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PulleyMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyMultiBodyDynamicsAnalysis',)


class PulleyMultiBodyDynamicsAnalysis(_5004.CouplingHalfMultiBodyDynamicsAnalysis):
    '''PulleyMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pulley_torque(self) -> 'List[float]':
        '''List[float]: 'PulleyTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.PulleyTorque)
        return value

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
    def peak_pulley_torque(self) -> 'List[_5107.DynamicTorqueResultAtTime]':
        '''List[DynamicTorqueResultAtTime]: 'PeakPulleyTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PeakPulleyTorque, constructor.new(_5107.DynamicTorqueResultAtTime))
        return value
