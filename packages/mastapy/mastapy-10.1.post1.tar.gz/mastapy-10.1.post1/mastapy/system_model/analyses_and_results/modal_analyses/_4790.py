'''_4790.py

RollingRingModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2129
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6170
from mastapy.system_model.analyses_and_results.system_deflections import _2302
from mastapy.system_model.analyses_and_results.modal_analyses import _4735
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'RollingRingModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingModalAnalysis',)


class RollingRingModalAnalysis(_4735.CouplingHalfModalAnalysis):
    '''RollingRingModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2129.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2129.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6170.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6170.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2302.RollingRingSystemDeflection':
        '''RollingRingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2302.RollingRingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[RollingRingModalAnalysis]':
        '''List[RollingRingModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingModalAnalysis))
        return value
