'''_4952.py

BeltConnectionMultiBodyDynamicsAnalysis
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _1360
from mastapy.system_model.connections_and_sockets import _1810
from mastapy.system_model.analyses_and_results.static_loads import _6032
from mastapy.system_model.analyses_and_results.mbd_analyses import _5010
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BeltConnectionMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionMultiBodyDynamicsAnalysis',)


class BeltConnectionMultiBodyDynamicsAnalysis(_5010.InterMountableComponentConnectionMultiBodyDynamicsAnalysis):
    '''BeltConnectionMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def extension(self) -> 'float':
        '''float: 'Extension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Extension

    @property
    def tension(self) -> 'float':
        '''float: 'Tension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Tension

    @property
    def loading_status(self) -> '_1360.LoadingStatus':
        '''LoadingStatus: 'LoadingStatus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.LoadingStatus)
        return constructor.new(_1360.LoadingStatus)(value) if value else None

    @property
    def connection_design(self) -> '_1810.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1810.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6032.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6032.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
