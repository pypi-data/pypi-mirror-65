'''_5445.py

CVTBeltConnectionSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1836
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5414
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CVTBeltConnectionSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionSingleMeshWhineAnalysis',)


class CVTBeltConnectionSingleMeshWhineAnalysis(_5414.BeltConnectionSingleMeshWhineAnalysis):
    '''CVTBeltConnectionSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1836.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1836.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
