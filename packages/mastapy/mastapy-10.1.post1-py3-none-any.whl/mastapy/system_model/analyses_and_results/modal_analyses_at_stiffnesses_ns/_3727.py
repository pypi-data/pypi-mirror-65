'''_3727.py

BeltConnectionModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets import _1831
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6054
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3780
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'BeltConnectionModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionModalAnalysesAtStiffnesses',)


class BeltConnectionModalAnalysesAtStiffnesses(_3780.InterMountableComponentConnectionModalAnalysesAtStiffnesses):
    '''BeltConnectionModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1831.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1831.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6054.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6054.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
