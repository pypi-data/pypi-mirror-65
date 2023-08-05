'''_4737.py

CVTBeltConnectionModalAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1836
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2246
from mastapy.system_model.analyses_and_results.modal_analyses import _4705
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CVTBeltConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionModalAnalysis',)


class CVTBeltConnectionModalAnalysis(_4705.BeltConnectionModalAnalysis):
    '''CVTBeltConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1836.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1836.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def system_deflection_results(self) -> '_2246.CVTBeltConnectionSystemDeflection':
        '''CVTBeltConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2246.CVTBeltConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
