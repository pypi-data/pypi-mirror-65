'''_4988.py

ClutchMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2112
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6068
from mastapy.system_model.analyses_and_results.mbd_analyses import _4986, _5005
from mastapy._internal.python_net import python_net_import

_CLUTCH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ClutchMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchMultiBodyDynamicsAnalysis',)


class ClutchMultiBodyDynamicsAnalysis(_5005.CouplingMultiBodyDynamicsAnalysis):
    '''ClutchMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2112.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2112.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6068.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6068.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def clutch_connection(self) -> '_4986.ClutchConnectionMultiBodyDynamicsAnalysis':
        '''ClutchConnectionMultiBodyDynamicsAnalysis: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4986.ClutchConnectionMultiBodyDynamicsAnalysis)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None
