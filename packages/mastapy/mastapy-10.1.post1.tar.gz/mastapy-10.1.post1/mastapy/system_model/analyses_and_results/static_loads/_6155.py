'''_6155.py

PartToPartShearCouplingConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets.couplings import _1899
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6084
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PartToPartShearCouplingConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionLoadCase',)


class PartToPartShearCouplingConnectionLoadCase(_6084.CouplingConnectionLoadCase):
    '''PartToPartShearCouplingConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1899.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1899.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
