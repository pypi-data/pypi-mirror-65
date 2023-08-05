'''_5822.py

ConceptGearMeshDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1865
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6075
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5848
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ConceptGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshDynamicAnalysis',)


class ConceptGearMeshDynamicAnalysis(_5848.GearMeshDynamicAnalysis):
    '''ConceptGearMeshDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1865.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1865.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6075.ConceptGearMeshLoadCase':
        '''ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6075.ConceptGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
