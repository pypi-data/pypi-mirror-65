'''_4984.py

BoltedJointMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6064
from mastapy.system_model.analyses_and_results.mbd_analyses import _5070
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BoltedJointMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointMultiBodyDynamicsAnalysis',)


class BoltedJointMultiBodyDynamicsAnalysis(_5070.SpecialisedAssemblyMultiBodyDynamicsAnalysis):
    '''BoltedJointMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1987.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6064.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6064.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
