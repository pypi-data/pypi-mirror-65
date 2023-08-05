'''_4789.py

RollingRingConnectionModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1851
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6169
from mastapy.system_model.analyses_and_results.system_deflections import _2301
from mastapy.system_model.analyses_and_results.modal_analyses import _4759
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'RollingRingConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionModalAnalysis',)


class RollingRingConnectionModalAnalysis(_4759.InterMountableComponentConnectionModalAnalysis):
    '''RollingRingConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1851.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1851.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6169.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6169.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2301.RollingRingConnectionSystemDeflection':
        '''RollingRingConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2301.RollingRingConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionModalAnalysis]':
        '''List[RollingRingConnectionModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionModalAnalysis))
        return value
