'''_5432.py

ConceptCouplingHalfSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2116
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6072
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5443
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ConceptCouplingHalfSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfSingleMeshWhineAnalysis',)


class ConceptCouplingHalfSingleMeshWhineAnalysis(_5443.CouplingHalfSingleMeshWhineAnalysis):
    '''ConceptCouplingHalfSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2116.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6072.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6072.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
