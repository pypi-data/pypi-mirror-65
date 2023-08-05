'''_5447.py

CVTSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2119
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5415
from mastapy._internal.python_net import python_net_import

_CVT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CVTSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTSingleMeshWhineAnalysis',)


class CVTSingleMeshWhineAnalysis(_5415.BeltDriveSingleMeshWhineAnalysis):
    '''CVTSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2119.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2119.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
