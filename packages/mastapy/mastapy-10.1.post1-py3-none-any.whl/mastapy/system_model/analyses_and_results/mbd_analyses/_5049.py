'''_5049.py

OilSealMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6152
from mastapy.system_model.analyses_and_results.mbd_analyses import _5002
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'OilSealMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealMultiBodyDynamicsAnalysis',)


class OilSealMultiBodyDynamicsAnalysis(_5002.ConnectorMultiBodyDynamicsAnalysis):
    '''OilSealMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6152.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6152.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[OilSealMultiBodyDynamicsAnalysis]':
        '''List[OilSealMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(OilSealMultiBodyDynamicsAnalysis))
        return value
