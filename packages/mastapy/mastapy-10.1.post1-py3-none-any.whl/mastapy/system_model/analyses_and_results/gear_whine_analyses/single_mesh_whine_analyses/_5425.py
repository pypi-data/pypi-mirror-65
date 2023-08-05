'''_5425.py

BoltSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _1986
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5430
from mastapy._internal.python_net import python_net_import

_BOLT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'BoltSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltSingleMeshWhineAnalysis',)


class BoltSingleMeshWhineAnalysis(_5430.ComponentSingleMeshWhineAnalysis):
    '''BoltSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1986.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6065.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6065.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
