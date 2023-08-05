'''_5046.py

MeasurementComponentMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2004
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6148
from mastapy.system_model.analyses_and_results.mbd_analyses import _5096
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MeasurementComponentMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentMultiBodyDynamicsAnalysis',)


class MeasurementComponentMultiBodyDynamicsAnalysis(_5096.VirtualComponentMultiBodyDynamicsAnalysis):
    '''MeasurementComponentMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2004.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6148.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6148.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
