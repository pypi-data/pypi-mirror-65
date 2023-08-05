'''_4051.py

RollingRingAssemblyModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2130
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6168
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4058
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'RollingRingAssemblyModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyModalAnalysesAtSpeeds',)


class RollingRingAssemblyModalAnalysesAtSpeeds(_4058.SpecialisedAssemblyModalAnalysesAtSpeeds):
    '''RollingRingAssemblyModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2130.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6168.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6168.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
