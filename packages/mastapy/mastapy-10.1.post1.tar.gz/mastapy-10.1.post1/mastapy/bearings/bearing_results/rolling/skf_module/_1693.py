'''_1693.py

Friction
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1694, _1695, _1704
from mastapy._internal.python_net import python_net_import

_FRICTION = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Friction')


__docformat__ = 'restructuredtext en'
__all__ = ('Friction',)


class Friction(_1704.SKFCalculationResult):
    '''Friction

    This is a mastapy class.
    '''

    TYPE = _FRICTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Friction.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def power_loss(self) -> 'float':
        '''float: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerLoss

    @property
    def frictional_moment(self) -> '_1694.FrictionalMoment':
        '''FrictionalMoment: 'FrictionalMoment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1694.FrictionalMoment)(self.wrapped.FrictionalMoment) if self.wrapped.FrictionalMoment else None

    @property
    def friction_sources(self) -> '_1695.FrictionSources':
        '''FrictionSources: 'FrictionSources' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1695.FrictionSources)(self.wrapped.FrictionSources) if self.wrapped.FrictionSources else None
