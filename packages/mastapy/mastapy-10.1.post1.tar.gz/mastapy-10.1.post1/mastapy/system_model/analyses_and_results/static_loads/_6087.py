'''_6087.py

CVTBeltConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets import _1836
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6054
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CVTBeltConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionLoadCase',)


class CVTBeltConnectionLoadCase(_6054.BeltConnectionLoadCase):
    '''CVTBeltConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1836.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1836.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
