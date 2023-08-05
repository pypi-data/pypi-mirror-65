'''_3961.py

BoltModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model import _1964
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6043
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3966
from mastapy._internal.python_net import python_net_import

_BOLT_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'BoltModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltModalAnalysesAtSpeeds',)


class BoltModalAnalysesAtSpeeds(_3966.ComponentModalAnalysesAtSpeeds):
    '''BoltModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _BOLT_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1964.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1964.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6043.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6043.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
