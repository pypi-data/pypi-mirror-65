'''_6054.py

BeltConnectionLoadCase
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.system_model.connections_and_sockets import _1831
from mastapy.system_model.analyses_and_results.static_loads import _6137
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BeltConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionLoadCase',)


class BeltConnectionLoadCase(_6137.InterMountableComponentConnectionLoadCase):
    '''BeltConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pre_extension(self) -> 'float':
        '''float: 'PreExtension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PreExtension

    @property
    def rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RayleighDampingBeta' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RayleighDampingBeta) if self.wrapped.RayleighDampingBeta else None

    @rayleigh_damping_beta.setter
    def rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RayleighDampingBeta = value

    @property
    def connection_design(self) -> '_1831.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1831.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
