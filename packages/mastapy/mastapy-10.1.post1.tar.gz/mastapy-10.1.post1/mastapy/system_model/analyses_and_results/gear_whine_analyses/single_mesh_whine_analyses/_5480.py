'''_5480.py

OilSealSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6152
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5441
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'OilSealSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealSingleMeshWhineAnalysis',)


class OilSealSingleMeshWhineAnalysis(_5441.ConnectorSingleMeshWhineAnalysis):
    '''OilSealSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealSingleMeshWhineAnalysis.TYPE'):
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
